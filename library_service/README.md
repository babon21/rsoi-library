+ Список книг в библиотеке. [G]
GET /library/{libraryUid}/books

Найти книгу в библиотеке. [S][G]
header: Authorization: bearer <jwt>
GET /library/book/{bookUid}

Взять книгу в библиотеке. [S][M][G]
header: Authorization: bearer <jwt>
POST /library/{libraryUid}/book/{bookUid}/take

Вернуть книгу. [S][M][G]
header: Authorization: bearer <jwt>
POST /library/{libraryUid}/book/{bookUid}/return

+ Добавить книгу в библиотеку. [A][M][G]
header: Authorization: bearer <jwt>
POST /library/{libraryUid}/book/{bookUid}

+ Убрать книгу из библиотеки. [A][M][G]
header: Authorization: bearer <jwt>
DELETE /library/{libraryUid}/book/{bookUid}

Посмотреть список взятых книг. [S][G]
header: Authorization: bearer <jwt>
GET /library/user/{userUid}/books
