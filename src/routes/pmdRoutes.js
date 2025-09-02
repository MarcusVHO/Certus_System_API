import express from "express";
import { getProgram } from "../core/programacao/progController.js";

const router = express.Router()

//Rota de de listagem de programações
router.post("/programacao", getProgram)


export default router