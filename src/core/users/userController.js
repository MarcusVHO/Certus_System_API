import {
  createUser,
  findUser,
  findUserByIdInDb,
  getRefreshToken,
  removeRefreshToken,
  updateRefreshToken,
} from "../../models/users/usersModel.js";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

// Está funcao é responsavel por registrar um novo usuário
export async function usersRegister(req, res) {
  try {
    const { name, oneid, password, confirmPassword, role } = req.body;

    //validação
    if (!name || !oneid || !password || !confirmPassword) {
      return res.status(422).json({ msg: "Todos os campos são obrigatórios" });
    }

    //Verifica se senha corresponde a confirm senha
    if (password != confirmPassword) {
      return res.status(401).json({ error: "Senhas não correspondem" });
    }

    //Verificar se usuario existe
    const userExist = await findUser(name, oneid);
    if (userExist) {
      console.log(`Usuário de nome: "${name}" já existe`);
      return res.status(422).json({ error: "Usuário já existe" });
    }

    //create password
    const salt = await bcrypt.genSalt(12);
    const passwordHash = await bcrypt.hash(password, salt);

    //create user
    try {
      const resposta = await createUser(name, oneid, passwordHash, role);
      console.log(`Usuário "${name}" criado com sucesso!! `);
      return res.status(201).json({ message: "Usuário criado com sucesso" });
    } catch (dbError) {
      res.status(500).json({ Erro: dbError.message });
    }
  } catch (err) {
    res.status(500).json({ error: "Erro ao registrar usuário" });
    console.log("Erro ao registrar usuário");
  }
}

//Está funcao é responsavel por logar um usuario
export async function userLogin(req, res) {
  try {
    const { oneid, password } = req.body;
    console.log(oneid, password);

    //Valida se todos os campos foram preenchidos
    if (!oneid || !password) {
      return res
        .status(401)
        .json({ message: "Todos os campos são obrigatórios" });
    }

    //Verifica se usuário existe
    const user = await findUser(null, oneid);
    if (!user) {
      console.log(`Usuário de oneid: "${oneid}" não encontrado`);
      return res.status(401).json({ error: "Usuário não encontrado" });
    }

    //Verfica se senha é igual a do banco
    const checkPassword = await bcrypt.compare(password, user.password);
    if (!checkPassword) {
      return res.status(401).json({ error: "Senha invalida" });
    }

    try {
      const secret = process.env.SECRET;

      //cria token e refresh token
      console.log(user);
      const token = jwt.sign({ name:user.name, oneid:user.oneid, id: user.id, role: user.role }, secret, {
        expiresIn: "30m",
      });
      const refreshToken = jwt.sign(
        { id: user.id },
        process.env.REFRESH_TOKEN_SECRET,
        { expiresIn: "9h" }
      );

      //atualizar refreshToken no banco de dados
      updateRefreshToken(refreshToken, user.id);

      //retorna ambos ao usuario
      res.cookie("refreshToken", refreshToken, {
        httpOnly: true,
        secure: true,
        sameSite: "strict"
      });
      res.status(200).json({ message: "Login efetuado com sucesso", token });
    } catch (error) {
      res.status(500).json({ error: "Erro ao criar id" });
    }
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

//Prucura usúarios através o oneid ROTA PRIVADA
export async function findUserById(req, res) {
  try {
    const id = req.params.id;

    //Procura usuário no banco
    const user = await findUserByIdInDb(id, null);
    if (!user) {
      console.log(`Usúário de id:${id} não encontrado `);
      return res.status(404).json({ message: "Usúário não encontrado" });
    }

    return res.status(200).json({ user });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}

//Gera um novo token apartir do refresh token
export async function getNewToken(req, res) {
  try {
    //obtem token do header
    const refresh_token = req.cookies.refreshToken
    //chave de seguranca
    const secret = process.env.REFRESH_TOKEN_SECRET;

    //verifica token
    const payload = jwt.verify(refresh_token, secret);
    console.log(payload);

    if (!payload) {
      return res.status(401).json({ message: "Acesso negado!" });
    }
    //pega refresh armazenado no banco de dados
    const tokenDb = await getRefreshToken(payload.id);
    console.log(tokenDb, refresh_token);

    if (tokenDb != refresh_token) {
      return res.status(401).json({ message: "Acesso negado!" });
    } else {
      const user = await findUser(payload.id, null);

      //cria token e refresh token
      const token = jwt.sign(
        { id: user.id, role: user.role },
        process.env.SECRET,
        { expiresIn: "30m" }
      );
      const refreshToken = jwt.sign(
        { id: user.id },
        process.env.REFRESH_TOKEN_SECRET,
        { expiresIn: "9h" }
      );

      //atualizar refreshToken no banco de dados
      updateRefreshToken(refreshToken, user.id);

      res.status(200).json({
        message: "Refresh Login efetuado com sucesso",
        token,
        refreshToken,
      });
    }

    //verifica token no banco de dados
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}


export async function userLogout(req, res) {
  try {
    const {id} = req.body

    const resposta = removeRefreshToken(id)
    if(resposta){
      res.status(200).json({message: "Logout Bem sucedido"})
    }
  } catch(error) {
    res.status(500).json({error: error.message})
  }
}