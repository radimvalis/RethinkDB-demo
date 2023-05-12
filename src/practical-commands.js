
/*

Run in web UI or with JavaScript driver

*/

// CREATE -------------------------------

// create database
r.dbCreate('my_database')

// list all databases
r.dbList()

// create table in database
r.db('my_database').tableCreate('users')

// list all tables in database
r.db('my_database').tableList()

// INSERT -----------------------------------

// insert data
r.db('my_database').table('users').insert({
    id: 1,
    age: 30,
    name: 'John'
})

// insert multiple data
r.db('my_database').table('users').insert([
    {
        id: 2,
        name: 'Peter',
        age: 25
    },
    {
        id: 3,
        name: 'George',
        age: 51
    }
])

// list all data in users table
r.db('my_database').table('users')

// show whole table and pluck
r.db('my_database').table('users')
    .pluck('id', 'name')

// filter
r.db('my_database').table('users').filter({
    name: 'Peter'
})

// filter & lt
r.db('my_database').table('users').filter(
    r.row.hasFields('age')
    .and(r.row('age').lt(40))
)

// order by
r.db('my_database').table('users').orderBy('age')

// UPDATE ---------------------------------

// update age
r.db('my_database').table('users').filter({
    name: 'George'
}).update({age: 40})

// DELETE --------------------------------

// delete one
r.db('my_database').table('users').filter({
    name: 'George'
}).delete()

// delete all data
//r.db('my_database').table('users').delete()

// JOIN

// add new table
r.db('my_database').tableCreate('posts')

r.db('my_database').table('posts').insert({
    id: 1,
    title: 'First Post',
    content: 'Constent of the post',
    authorId: 1
})

// join
r.db('my_database').table('posts').innerJoin(
    r.db('my_database').table('users'),
    function (post, user) {
        return post('authorId').eq(user('id'));
}).zip()

// DROP --------------------------------

// drop table
r.db('my_database').tableDrop('users')

// drop database
r.dbDrop('my_database')
