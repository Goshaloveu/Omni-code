import express from "express"
import mysql from "mysql2"
import cors from "cors"

const app = express()

const db = mysql.createConnection({
    host:"localhost",
    user:"root",
    password:"S@nktum56",
    database:"people"
})

app.use(cors())

// app.get("/", (req, res) => {
//     res.json("hello this is the backend!")
// })

app.get("/", (req, res) => {
    const q = "SELECT * FROM people.users;";
    db.query(q, (err, data) => {
        if (err) return res.json(err);
        res.json(data);
    })
})

app.get("/3", (req, res) => {
    const q = "SELECT * FROM people.users WHERE reiting <= 30;";
    db.query(q, (err, data) => {
        if (err) return res.json(err);
        res.json(data);
    })
})

app.get("/2", (req, res) => {
    const q = "SELECT * FROM people.users WHERE 30 < reiting and reiting <= 60;";
    db.query(q, (err, data) => {
        if (err) return res.json(err);
        res.json(data);
    })
})

app.get("/1", (req, res) => {
    const q = "SELECT * FROM people.users WHERE 60 < reiting;";
    db.query(q, (err, data) => {
        if (err) return res.json(err);
        res.json(data);
    })
})

app.listen(5000, () => {
    console.log("Connected to backend!");
})