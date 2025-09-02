import { getProgramDb } from "../../models/programacao/progModel.js"


export async function getProgram(req, res) {
    try {
        const {data1, data2} = req.body
        const itens = await getProgramDb(data1, data2)
        console.log(`Procurando Data1: ${data1}, Data2: ${data2}, resultado ${itens}`);

        res.status(201).json({programacoes: itens})
    } catch(error) {
        res.status(500).json({message: error.message})
    }
}