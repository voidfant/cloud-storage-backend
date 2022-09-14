import pymysql.cursors


class SQLInteractor(object):

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='19Andrew76',
                                     database='killedPrev',
                                     cursorclass=pymysql.cursors.DictCursor)

    def checkId(self, elementId: str) -> str:
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = f"SELECT type FROM dfrApp_element WHERE id = '{elementId}'"
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return result['type']
                else:
                    return ''

    def getElement(self, elementId: str) -> dict:
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = f"SELECT * FROM dfrApp_element WHERE id = '{elementId}'"
                cursor.execute(sql)

                return cursor.fetchone()

    def getChildren(self, elementId: str) -> list:
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = f"SELECT * FROM dfrApp_element WHERE parentId = '{elementId}'"
                cursor.execute(sql)

                return cursor.fetchall()

    def getParentType(self, elementId: str) -> str:
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = f'SELECT parentId FROM dfrApp_element WHERE id = "{elementId}"'
                cursor.execute(sql)
                parent = cursor.fetchone()['parentId']
                sql = f'SELECT type, id FROM dfrApp_element WHERE id = "{parent}"'
                cursor.execute(sql)
                result = cursor.fetchone()
                if result:
                    return result['type']

                return ''

    def updateElement(self, data: dict) -> None:
        elementId = data['id']
        del data['id']

        with self.connection:
            with self.connection.cursor() as cursor:
                for k, v in data.items():
                    if not v:
                        sql = f"UPDATE killedPrev.dfrapp_element SET {k} = NULL WHERE id = '{elementId}'"
                    elif isinstance(v, int):
                        sql = f"UPDATE killedPrev.dfrapp_element SET {k} = {v} WHERE id = '{elementId}'"
                    else:
                        sql = f"UPDATE killedPrev.dfrapp_element SET {k} = '{v}' WHERE id = '{elementId}'"
                    cursor.execute(sql)
            self.connection.commit()

    def getFolderSize(self, elementId: str) -> int:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='19Andrew76',
                                     database='killedPrev',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = f'SELECT id, type, size FROM dfrApp_element WHERE parentId = "{elementId}"'
                cursor.execute(sql)
                result = cursor.fetchall()
                size = 0
                for v in result:
                    if v['type'] == 'FILE':
                        size += v['size']
                    else:
                        size += self.getFolderSize(v['id'])
                sql = f'UPDATE killedPrev.dfrapp_element SET size = "{size}" WHERE id = "{elementId}"'
                cursor.execute(sql)
            connection.commit()

            return size

    def getChildrenIds(self, elementId: str) -> list:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='19Andrew76',
                                     database='killedPrev',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = f'SELECT id, type FROM dfrApp_element WHERE parentId = "{elementId}"'
                cursor.execute(sql)
                result = cursor.fetchall()
                ids = [elementId]
                for v in result:
                    if v['type'] == 'FILE':
                        ids.append(v['id'])
                    else:
                        ids.append(v['id'])
                        ids.extend(self.getChildrenIds(v['id']))

                return ids

    def deleteElement(self, elementIds: list) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                for el in elementIds:
                    sql = f'DELETE FROM killedPrev.dfrApp_element WHERE id = "{el}"'
                    cursor.execute(sql)
            self.connection.commit()

    def clearTable(self) -> None:
        with self.connection:
            with self.connection.cursor() as cursor:
                sql = 'DELETE FROM killedPrev.dfrApp_element WHERE id != "-!<-!!>-"'
                cursor.execute(sql)
            self.connection.commit()

    def getParentsIds(self, elementId: str) -> list:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='19Andrew76',
                                     database='killedPrev',
                                     cursorclass=pymysql.cursors.DictCursor)
        with connection:
            with connection.cursor() as cursor:
                sql = f'SELECT parentId FROM dfrApp_element WHERE id = "{elementId}"'
                cursor.execute(sql)
                result = cursor.fetchone()
                ids = []
                while result:
                    ids.append(result['parentId'])
                    elementId = result['parentId']

                    sql = f'SELECT parentId FROM dfrApp_element WHERE id = "{elementId}"'
                    cursor.execute(sql)
                    result = cursor.fetchone()

                return [x for x in ids if x is not None]

    def updateDateOnInteraction(self, elementId, date):
        with self.connection:
            with self.connection.cursor() as cursor:
                affectedIds = self.getParentsIds(elementId)
                print(affectedIds)
                for i in affectedIds:
                    sql = f'UPDATE killedPrev.dfrapp_element SET date = "{date}" WHERE id = "{i}"'
                    cursor.execute(sql)

            self.connection.commit()


