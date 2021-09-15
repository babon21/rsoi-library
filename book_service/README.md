[S] – требуют авторизации;

[G] – запрос проходит через Gateway Service.

[A] – требуют авторизации и прав администратора;

[M] – операция модификации.


#### + Подробная информация о книге. [G]
GET /books/{bookUid}
#### Поиск по названию книги. [G]
GET /books?name=...& author=...
#### Информация об авторе. [G]
GET /author/{authorUid}
#### Краткая информация об авторе и список его книг. [G]
GET /author/{authorUid}/books
#### + Добавить книгу. [A][M][G]
header: Authorization: bearer <jwt>
POST /books/{bookUid}
body: { name, author, gerne }
#### + Удалить книгу. [A][M][G]
header: Authorization: bearer <jwt>
DELETE /books/{bookUid}
