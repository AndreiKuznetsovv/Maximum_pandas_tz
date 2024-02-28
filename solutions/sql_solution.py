import pandas as pd
from sqlalchemy import text

from database import CConnection, session_scope

""" В данном модуле описано решение задачи с помощью 'сырого' SQL """


class SQLSolution:
    """  """
    connection = CConnection()

    def get_data(self):
        with session_scope(self.connection) as session:
            query = session.execute(
                text(
                    """
                    SELECT c.communication_id,
                           c.site_id,
                           c.visitor_id,
                           c.date_time,
                           s.visitor_session_id,
                           s.date_time,
                           s.campaign_id,
                           ROW_NUMBER() OVER(PARTITION BY c.site_id, c.visitor_id ORDER BY s.date_time DESC) AS row_n
                    FROM web_data.communications c
                        LEFT JOIN web_data.sessions s
                            ON c.site_id = s.site_id
                                AND c.visitor_id = s.visitor_id
                                AND c.date_time > s.date_time
                    GROUP BY c.communication_id,
                             s.visitor_session_id,
                             c.date_time,
                             s.date_time,
                             s.campaign_id
                    ORDER BY c.communication_id;
                    """
                )
            ).fetchall()

            result = pd.DataFrame.from_records(
                query,
                columns=[
                    'communication_id', 'site_id', 'visitor_id',
                    'date_time', 'visitor_session_id', 'date_time',
                    'campaign_id', 'row_n'
                ]
            )

        return result
