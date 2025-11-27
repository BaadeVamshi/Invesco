const exp=require('express')
const app=exp();
require('dotenv').config()
const mongoClient=require('mongodb').MongoClient

app.use(exp.json())

// mount user API routes
const userApi = require('./API/user-api')
app.use('/user-api', userApi)

mongoClient.connect(process.env.DB_URL)
.then(client=>{
    const dbObj=client.db('budgetdb')
    const usersCollection=dbObj.collection('usersCollection')
    app.set('userscollection',usersCollection)
    console.log("connection to DB successful")
})
.catch(err=>console.log("error is ",err))



const port=process.env.PORT || 5000
app.listen(port,()=>console.log("server starting at port",4000))