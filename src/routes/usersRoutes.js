import express from "express";
import { findUserById, getNewToken, userLogin, userLogout, usersRegister } from "../core/users/userController.js";
import { checkToken } from "../middlewares/authMiddwares.js";

const router = express.Router();

//Rota para registrar usuário
router.post("/register", usersRegister);

//Rota de login de usuário
router.post("/login", userLogin)

//Procura usúrio por id
router.get("/finduserbyid/:id", checkToken, findUserById)

//pede um novo refreshtoken
router.get("/getnewtoken", getNewToken)

//faz logout 
router.post("/logout", userLogout)

export default router;
