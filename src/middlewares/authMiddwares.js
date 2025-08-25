import jwt from "jsonwebtoken"
import { findUserByIdInDb } from "../models/users/usersModel.js"


// Este midware verifica se token existe e é valido
export async function checkToken(req, res, next) {
    try {

        const authHeader = req.headers['authorization']
        const token = authHeader && authHeader.split(" ")[1]

        //Verifica se token foi enviado na requisição
        if(!token) {
            return res.status(401).json({message: "Acesso negado!"})
        }

        try {
            const secret = process.env.SECRET
            

            //verfica se token é valido
            const payload = jwt.verify(token, secret)
            console.log(payload)

            //verfica se usuário existe
            const user = await findUserByIdInDb(payload.id, payload.oneid)
            console.log(user)
            

            if(!user) {
                return res.status(400).json({message: "Acesso negado!"})
            }
            req.user = payload
            next()

        } catch(error) {
            res.status(400).json({error: "Token Invalido"})
        }

    } catch(error) {
        res.status(500).json({error: error.message})
    }
}