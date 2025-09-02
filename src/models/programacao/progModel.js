import connection from "../../database/database.js";


export async function getProgramDb(data1, data2) {
    const resposta = await connection.query(
        "SELECT * FROM programDays WHERE DATE(data) BETWEEN ? AND ?;",[data1, data2]
    )

    return resposta[0]
}