from pytest import mark


@mark.asyncio
async def test_qwe(db_connection):
    await db_connection.execute(
        'insert into categories ("name", "description") values ($1, $2)',
        "test name",
        "test description"
    )
    r = await db_connection.fetchrow('select * from categories')
    print(r)
