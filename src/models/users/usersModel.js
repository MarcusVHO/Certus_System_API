import connection from "../../database/database.js";

// Procura usuários
export async function findUser(id, oneid) {
  try {
    const [row] = await connection.query(
      "SELECT id, name, oneid, password, role FROM users WHERE id = ? OR oneid = ?",
      [id, oneid]
    );

    if (row.length > 0) {
      return row[0];
    } else {
      return null;
    }
  } catch (error) {
    throw error;
  }
}

//Cria usuarios no banco de dados
export async function createUser(name, oneid, password, role) {
  try {
    const [row] = await connection.query(
      "INSERT INTO users (name, oneid, password, role) VALUES (?, ?, ?, ?)",
      [name, Number(oneid), password, role]
    );
  } catch (error) {
    console.log(error);
    throw error;
  }
}

//Procura usuário por id sem retornar a senha
export async function findUserByIdInDb(id, oneid) {
    try {
        const [row] = await connection.query("SELECT id, name, oneid FROM users WHERE id = ? OR oneid = ?", [id, oneid])

        if (row.length > 0) {
            return row[0]
        } else {
            return null
        }
    } catch(error) {
        throw error
    }
}


//faz update do refresh token no banco de dados
export async function updateRefreshToken(refreshToken, id) {
    await connection.query(
        "UPDATE users SET refresh_token = ? WHERE id = ?", [refreshToken, id]
    )
}


export async function getRefreshToken(id) {
  const resposta =  await connection.query(
    "SELECT refresh_token FROM users WHERE id = ?",[id]
  )

  return resposta[0][0].refresh_token
}


export async function removeRefreshToken(id) {
  const resposta = await connection.query(
    "UPDATE users SET refresh_token = '' WHERE id = ?", [id]
  )
  return resposta
}