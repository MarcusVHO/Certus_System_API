import express from "express"
import cors from "cors"
import connection from "./database/database.js"
import usersRoutes from "./routes/usersRoutes.js"
import pmdRoutes from "./routes/pmdRoutes.js"
console.log("Starting Server .....")

//configs do express
const app = express()
app.use(express.json())
app.use(cors())

//teste da api
app.get("/status", (req, res) => {
    res.status(200).json({msg:"Bem vindo a nossa API!"})
    console.log("oi")
})

//Rotas da api
app.use("/users", usersRoutes)

app.use("/pmd", pmdRoutes)

app.listen(3000)