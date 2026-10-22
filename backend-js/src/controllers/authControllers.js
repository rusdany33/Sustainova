const db = require("../config/db");
const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const queryAsync = require("../utils/db");

// USer Login Function
exports.loginUser = async (req, res) => {
  try {
    const email = typeof req.body?.email === 'string' ? req.body.email.trim() : '';
    const password = typeof req.body?.password === 'string' ? req.body.password : '';

    // Validasi input
    const errors = {};
    if (!email) errors.email = 'Email wajib diisi';
    else if (email.length > 255 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) errors.email = 'Format email tidak valid';
    if (!password) errors.password = 'Password wajib diisi';
    if (Object.keys(errors).length) {
      return res.status(400).json({
        success: false,
        message: Object.values(errors)[0],
        errors,
      });
    }

    // Cek apakah email terdaftar
    const users = await queryAsync("SELECT * FROM users WHERE email = ?", [email]);
    if (users.length === 0) {
      return res.status(401).json({
        success: false,
        message: "Email tidak terdaftar",
        field: 'email',
        errors: { email: 'Email tidak terdaftar' },
      });
    }

    const user = users[0];

    // Cek password
    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      return res.status(401).json({
        success: false,
        message: "Password salah",
        field: 'password',
        errors: { password: 'Password salah' },
      });
    }

    // Generate JWT token
    const token = jwt.sign(
      {
        ID_user: user.ID_user,
        email: user.email,
        role: user.role || "user",
        session_version: user.session_version || 0,
      },
      process.env.JWT_SECRET,
      { expiresIn: "1d" }
    );

    // Kirim respon
    res.json({
      success: true,
      message: "Login berhasil",
      token,
      user: {
        id: user.ID_user,
        name: user.name,
        email: user.email,
        role: user.role,
      },
    });

  } catch (error) {
    // console.error("Error saat login:", error);
    res.status(500).json({
      success: false,
      message: "Terjadi kesalahan saat login",
    });
  }
};

// User Registration Function
exports.registerUser = async (req, res) => {
  try {
    const { name, email, telephone, address, password } = req.body;

    // Validasi input
    if (!name || !email || !password) {
      return res.status(400).json({
        success: false,
        message: "Nama, email, dan password wajib diisi",
      });
    }

    // Cek apakah email sudah terdaftar
    const existingUser = await queryAsync("SELECT email FROM users WHERE email = ?", [email]);
    if (existingUser.length > 0) {
      return res.status(400).json({
        success: false,
        message: "Email sudah terdaftar",
      });
    }

    // Enkripsi password
    const hashedPassword = await bcrypt.hash(password, 10);

    // Data user yang akan disimpan
    const userData = {
      name,
      email,
      telephone: telephone || null,
      address: address || null,
      password: hashedPassword,
      role: "user",
    };

    // Simpan user ke database
    const result = await queryAsync("INSERT INTO users SET ?", userData);

    // Respon sukses
    res.status(201).json({
      success: true,
      message: "Pendaftaran berhasil",
      data: {
        userId: result.insertId,
        name: userData.name,
        email: userData.email,
      },
    });

  } catch (error) {
    // console.error("Error saat registrasi:", error);
    res.status(500).json({
      success: false,
      message: "Terjadi kesalahan server",
    });
  }
};
