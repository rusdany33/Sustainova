/**
 * Unit Testing - Fitur Register (authControllers.registerUser)
 * PKPL Modul 4 - White-Box Testing & Unit Testing
 *
 * Unit yang diuji : exports.registerUser di src/controllers/authControllers.js
 * Framework       : Jest
 * Pola            : Arrange - Act - Assert (AAA)
 *
 * Test Double yang dipakai:
 *  - Dummy : modul koneksi database (src/config/db) -> wajib di-require oleh
 *            controller, tetapi tidak dipakai oleh registerUser.
 *  - Stub  : queryAsync (src/utils/db) -> mengembalikan hasil query yang sudah
 *            ditentukan (email sudah ada / belum ada / error database).
 *  - Mock  : objek res Express -> memverifikasi status() dan json() dipanggil
 *            dengan argumen yang benar.
 *  - Fake  : FakeUserRepository -> database users in-memory yang benar-benar
 *            menyimpan data, sehingga skenario "daftar dua kali" bisa diuji.
 *  - Spy   : jest.spyOn(bcrypt, "hash") -> merekam pemanggilan hash password
 *            tanpa mengganti implementasi aslinya.
 */

// ===== Dummy: koneksi database asli tidak boleh dibuat saat unit test =====
jest.mock("../../src/config/db", () => ({}));

// ===== Stub/Fake: queryAsync diganti jest.fn agar perilakunya bisa diatur =====
jest.mock("../../src/utils/db", () => jest.fn());

const bcrypt = require("bcrypt");
const queryAsync = require("../../src/utils/db");
const { registerUser } = require("../../src/controllers/authControllers");

// Helper: Mock untuk objek response Express
function createMockResponse() {
  const res = {};
  res.status = jest.fn().mockReturnValue(res);
  res.json = jest.fn().mockReturnValue(res);
  return res;
}

// Helper: Fake repository users (in-memory) yang meniru tabel users MySQL
class FakeUserRepository {
  constructor() {
    this.users = [];
    this.nextId = 1;
  }

  query(sql, params) {
    if (sql.startsWith("SELECT email FROM users WHERE email = ?")) {
      const [email] = params;
      return Promise.resolve(
        this.users.filter((u) => u.email === email).map((u) => ({ email: u.email }))
      );
    }
    if (sql.startsWith("INSERT INTO users SET ?")) {
      const row = { ID_user: this.nextId++, ...params };
      this.users.push(row);
      return Promise.resolve({ insertId: row.ID_user });
    }
    return Promise.reject(new Error(`Query tidak dikenal: ${sql}`));
  }
}

const validBody = {
  name: "Rusdany Maestro",
  email: "rusdany.test@example.com",
  telephone: "081234567890",
  address: "Jl. Raya Tlogomas No. 246, Malang",
  password: "rahasia123",
};

describe("registerUser - White-Box Unit Test", () => {
  let hashSpy;

  beforeEach(() => {
    queryAsync.mockReset();
    // Spy: bcrypt.hash asli tetap berjalan, pemanggilannya direkam
    hashSpy = jest.spyOn(bcrypt, "hash");
  });

  afterEach(() => {
    hashSpy.mockRestore();
  });

  // TC-01 | Jalur: S1, S2(True), S3 | Branch: B1, B10
  test("TC-01: menolak registrasi jika name, email, atau password kosong (400)", async () => {
    // Arrange
    const req = { body: { name: "", email: "kosong@example.com", password: "" } };
    const res = createMockResponse();

    // Act
    await registerUser(req, res);

    // Assert
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({
      success: false,
      message: "Nama, email, dan password wajib diisi",
    });
    expect(queryAsync).not.toHaveBeenCalled();
    expect(hashSpy).not.toHaveBeenCalled();
  });

  // TC-02 | Jalur: S1, S2(False), S4, S5(True), S6 | Branch: B2, B3, B10
  test("TC-02: menolak registrasi jika email sudah terdaftar (400) - Stub", async () => {
    // Arrange
    queryAsync.mockResolvedValueOnce([{ email: validBody.email }]); // Stub: email sudah ada
    const req = { body: { ...validBody } };
    const res = createMockResponse();

    // Act
    await registerUser(req, res);

    // Assert
    expect(queryAsync).toHaveBeenCalledTimes(1);
    expect(queryAsync).toHaveBeenCalledWith(
      "SELECT email FROM users WHERE email = ?",
      [validBody.email]
    );
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({
      success: false,
      message: "Email sudah terdaftar",
    });
    expect(hashSpy).not.toHaveBeenCalled();
  });

  // TC-03 | Jalur: S1, S2(F), S4, S5(F), S7, S8(tel & address terisi), S9, S10 | Branch: B2, B4, B5, B7, B10
  test("TC-03: registrasi berhasil dengan data lengkap, role selalu 'user' (201) - Stub + Spy", async () => {
    // Arrange
    queryAsync
      .mockResolvedValueOnce([]) // Stub: email belum terdaftar
      .mockResolvedValueOnce({ insertId: 42 }); // Stub: hasil INSERT
    const req = { body: { ...validBody } };
    const res = createMockResponse();

    // Act
    await registerUser(req, res);

    // Assert - Spy bcrypt.hash
    expect(hashSpy).toHaveBeenCalledTimes(1);
    expect(hashSpy).toHaveBeenCalledWith(validBody.password, 10);

    // Assert - data yang dikirim ke INSERT
    const [insertSql, userData] = queryAsync.mock.calls[1];
    expect(insertSql).toBe("INSERT INTO users SET ?");
    expect(userData).toMatchObject({
      name: validBody.name,
      email: validBody.email,
      telephone: validBody.telephone,
      address: validBody.address,
      role: "user",
    });
    expect(userData.password).not.toBe(validBody.password);
    expect(await bcrypt.compare(validBody.password, userData.password)).toBe(true);

    // Assert - Mock response
    expect(res.status).toHaveBeenCalledWith(201);
    expect(res.json).toHaveBeenCalledWith({
      success: true,
      message: "Pendaftaran berhasil",
      data: { userId: 42, name: validBody.name, email: validBody.email },
    });
  });

  // TC-04 | Jalur: S1, S2(F), S4, S5(F), S7, S8(tel & address kosong), S9, S10 | Branch: B2, B4, B6, B8, B10
  test("TC-04: telephone dan address opsional disimpan sebagai null (201)", async () => {
    // Arrange
    queryAsync.mockResolvedValueOnce([]).mockResolvedValueOnce({ insertId: 7 });
    const req = {
      body: { name: "User Minimal", email: "minimal@example.com", password: "rahasia123" },
    };
    const res = createMockResponse();

    // Act
    await registerUser(req, res);

    // Assert
    const userData = queryAsync.mock.calls[1][1];
    expect(userData.telephone).toBeNull();
    expect(userData.address).toBeNull();
    expect(res.status).toHaveBeenCalledWith(201);
  });

  // TC-05 | Jalur: S1, S2(F), S4 -> exception, S11 | Branch: B2, B9
  test("TC-05: mengembalikan 500 jika database gagal - Stub error", async () => {
    // Arrange
    queryAsync.mockRejectedValueOnce(new Error("ECONNREFUSED")); // Stub: DB down
    const req = { body: { ...validBody } };
    const res = createMockResponse();

    // Act
    await registerUser(req, res);

    // Assert
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({
      success: false,
      message: "Terjadi kesalahan server",
    });
    expect(hashSpy).not.toHaveBeenCalled();
  });

  // TC-06 | Fake repository: daftar pertama berhasil, daftar kedua dengan email sama ditolak
  test("TC-06: email yang sama tidak dapat didaftarkan dua kali - Fake", async () => {
    // Arrange
    const fakeRepo = new FakeUserRepository();
    queryAsync.mockImplementation((sql, params) => fakeRepo.query(sql, params));
    const firstRes = createMockResponse();
    const secondRes = createMockResponse();

    // Act
    await registerUser({ body: { ...validBody } }, firstRes);
    await registerUser({ body: { ...validBody, name: "Akun Kembar" } }, secondRes);

    // Assert
    expect(firstRes.status).toHaveBeenCalledWith(201);
    expect(secondRes.status).toHaveBeenCalledWith(400);
    expect(secondRes.json).toHaveBeenCalledWith({
      success: false,
      message: "Email sudah terdaftar",
    });
    expect(fakeRepo.users).toHaveLength(1);
    expect(fakeRepo.users[0]).toMatchObject({ email: validBody.email, role: "user" });
  });
});
