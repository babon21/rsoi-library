Взять книгу в библиотеке. [S][M][G]
header: Authorization: bearer <jwt>
POST /library/{libraryUid}/book/{bookUid}/take

Вернуть книгу. [S][M][G]
header: Authorization: bearer <jwt>
POST /library/{libraryUid}/book/{bookUid}/return
