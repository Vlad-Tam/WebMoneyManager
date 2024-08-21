from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.orm import outerjoin, Session

from src.categories.models import CategoriesOrm
from src.categories.schemas import CategoryDTO
from src.db.database import session
from src.transactions.models import TransactionsOrm
from src.transactions.schemas import TransactionDTO
from src.users.models import UserOrm
from src.users.schemas import UserDTO
from sqlalchemy import select, func, extract, text


class HomeRepository:
    @classmethod
    async def get_homepage_info(cls, user_id: int, time_period: Optional[str] = "month") -> dict:
        async with session() as new_session:
            query = """
                        SELECT
                            u.name,
                            u.surname,
                            u.email,
                            u.main_currency,
                            u.month_limit,
                            u.birth_date,
                            (
                                SELECT
                                    value
                                FROM transaction
                                WHERE user_id = u.id
                                ORDER BY created_at DESC
                                LIMIT 1
                            ) AS last_spending_value,
                            (
                                SELECT
                                    description
                                FROM transaction
                                WHERE user_id = u.id
                                ORDER BY created_at DESC
                                LIMIT 1
                            ) AS last_spending_description,
                            (
                                SELECT
                                    created_at
                                FROM transaction
                                WHERE user_id = u.id
                                ORDER BY created_at DESC
                                LIMIT 1
                            ) AS last_spending_time,
                            (
                                SELECT
                                    SUM(t.value)
                                FROM transaction t
                                WHERE t.user_id = u.id
                                AND t.operation_type = 'sub'
                                AND CASE
                                    WHEN :time_period = 'month' THEN DATE_TRUNC('month', t.created_at) = DATE_TRUNC('month', NOW())
                                    WHEN :time_period = 'year' THEN DATE_TRUNC('year', t.created_at) = DATE_TRUNC('year', NOW())
                                    WHEN :time_period = 'week' THEN DATE_TRUNC('week', t.created_at) = DATE_TRUNC('week', NOW())
                                END
                            ) AS current_sub,
                            (
                                SELECT
                                    SUM(t.value)
                                FROM transaction t
                                WHERE t.user_id = u.id
                                AND t.operation_type = 'sub'
                                AND DATE_TRUNC('month', t.created_at) = DATE_TRUNC('month', NOW())
                            ) AS current_month_sub,
                            ((
                                SELECT
                                    SUM(t.value)
                                FROM transaction t
                                WHERE t.user_id = u.id
                                AND t.operation_type = 'add'
                            ) -
                            (
                                SELECT
                                    SUM(t.value)
                                FROM transaction t
                                WHERE t.user_id = u.id
                                AND t.operation_type = 'sub'
                            )) AS current_balance
                        FROM "user" AS u
                        WHERE u.id = :user_id;
                    """
            result = await new_session.execute(text(query), {'user_id': user_id, 'time_period': time_period})
            user_data = result.unique().mappings().one_or_none()
            return user_data
