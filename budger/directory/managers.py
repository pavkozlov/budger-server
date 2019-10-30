from django.db import models
from django.db import connection


class KsoManager(models.Manager):
    def list(self):
        with connection.cursor() as cursor:

            sql = '''
                SELECT
                    directory_kso.id,
                    directory_kso.title_full,
                    directory_kso.in_alliance,
                    directory_kso.worker_count_staff,
                    COUNT(emp_1.*),

                    emp_2.id,
                    emp_2.name,
                    emp_2."position",
                    emp_2.photo_slug
                
                FROM directory_kso

                LEFT JOIN directory_ksoemployee AS emp_2 ON emp_2.kso_id = directory_kso.id AND emp_2.is_head = TRUE
                LEFT JOIN directory_ksoemployee AS emp_1 ON emp_1.kso_id = directory_kso.id

                GROUP BY directory_kso.id, emp_2.id
                ORDER BY directory_kso.id
            '''

            cursor.execute(sql)

            result_list = []

            for row in cursor.fetchall():
                m = self.model(
                    id=row[0],
                    title_full=row[1],
                    in_alliance=row[2],
                    worker_count_staff=row[3],
                    worker_count_fact=row[4]
                )
                m.head = {
                    'id': row[5],
                    'name': row[6],
                    'position': row[7],
                    'photo_slug': row[8],
                }
                result_list.append(m)

        return result_list
