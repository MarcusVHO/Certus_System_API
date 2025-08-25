import "dotenv/config"
import mysql from "mysql2/promise";

const dbUser = process.env.DB_USER
const dbPass = process.env.DB_PASS
const dbHost = process.env.DB_HOST



const connection = mysql.createPool({
  host: dbHost,
  user: dbUser,
  password: dbPass,
  database: "CERTUS",
  connectionLimit: 10,
});

console.log("Conexao estabelicida com sucesso");

export default connection;
