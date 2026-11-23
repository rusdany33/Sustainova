/**
 * Unit Testing - Fitur Login (authControllers.loginUser)
 * Pendukung fitur Register: akun hasil registrasi dipakai untuk login.
 *
 * Test Double:
 *  - Dummy : src/config/db (tidak dipakai oleh loginUser)
 *  - Stub  : queryAsync mengembalikan user tetap / kosong / error
 *  - Stub  : bcrypt.compare dan jwt.sign dengan nilai kembalian tetap
 *  - Mock  : objek res Express
 */

jest.mock("../../src/config/db", () => ({}));
jest.mock("../../src/utils/db", () => jest.fn());

const bcrypt = require("bcrypt");
const jwt = require("jsonwebtoken");
const queryAsync = require("../../src/utils/db");
const { loginUser } = require("../../src/controllers/authControllers");

function createMockResponse() {
  const res = {};
  res.status = jest.fn().mockReturnValue(res);
  res.json = jest.fn().mockReturnValue(res);
  return res;
}

const storedUser = {
  ID_user: 5,
  name: "Rusdany Maestro",
  email: "rusdany.test@example.com",
  password: "$2b$10$hashpalsu",
  role: "user",
  session_version: 0,
};

describe("loginUser - White-Box Unit Test", () => {
  beforeEach(() => {
    queryAsync.mockReset();
    jest.restoreAllMocks();
    process.env.JWT_SECRET = "jwt-secret-untuk-test";
  });

  test("LG-01: email dan password kosong ditolak (400)", async () => {
    // Arrange
    const res = createMockResponse();

    // Act
    await loginUser({ body: {} }, res);

    // Assert
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json).toHaveBeenCalledWith({
      success: false,
      message: "Email wajib diisi",
      errors: { email: "Email wajib diisi", password: "Password wajib diisi" },
    });
    expect(queryAsync).not.toHaveBeenCalled();
  });

  test("LG-02: format email tidak valid ditolak (400)", async () => {
    // Arrange
    const res = createMockResponse();

    // Act
    await loginUser({ body: { email: "bukan-email", password: "rahasia123" } }, res);

    // Assert
    expect(res.status).toHaveBeenCalledWith(400);
    expect(res.json.mock.calls[0][0].errors).toEqual({ email: "Format email tidak valid" });
  });

  test("LG-03: email tidak terdaftar ditolak (401) - Stub query kosong", async () => {
    // Arrange
    queryAsync.mockResolvedValueOnce([]);
    const res = createMockResponse();

    // Act
    await loginUser({ body: { email: "  baru@example.com  ", password: "x" } }, res);

    // Assert
    expect(queryAsync).toHaveBeenCalledWith("SELECT * FROM users WHERE email = ?", [
      "baru@example.com",
    ]);
    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json.mock.calls[0][0].field).toBe("email");
  });

  test("LG-04: password salah ditolak (401) - Stub bcrypt.compare", async () => {
    // Arrange
    queryAsync.mockResolvedValueOnce([storedUser]);
    jest.spyOn(bcrypt, "compare").mockResolvedValue(false);
    const res = createMockResponse();

    // Act
    await loginUser({ body: { email: storedUser.email, password: "salah" } }, res);

    // Assert
    expect(res.status).toHaveBeenCalledWith(401);
    expect(res.json.mock.calls[0][0].field).toBe("password");
  });

  test("LG-05: kredensial benar menghasilkan token (200) - Stub bcrypt & jwt", async () => {
    // Arrange
    queryAsync.mockResolvedValueOnce([storedUser]);
    jest.spyOn(bcrypt, "compare").mockResolvedValue(true);
    const signStub = jest.spyOn(jwt, "sign").mockReturnValue("token-palsu");
    const res = createMockResponse();

    // Act
    await loginUser({ body: { email: storedUser.email, password: "rahasia123" } }, res);

    // Assert
    expect(signStub).toHaveBeenCalledWith(
      { ID_user: 5, email: storedUser.email, role: "user", session_version: 0 },
      "jwt-secret-untuk-test",
      { expiresIn: "1d" }
    );
    expect(res.status).not.toHaveBeenCalled();
    expect(res.json).toHaveBeenCalledWith({
      success: true,
      message: "Login berhasil",
      token: "token-palsu",
      user: { id: 5, name: storedUser.name, email: storedUser.email, role: "user" },
    });
  });

  test("LG-06: role/session_version kosong memakai nilai default", async () => {
    // Arrange
    queryAsync.mockResolvedValueOnce([{ ...storedUser, role: null, session_version: null }]);
    jest.spyOn(bcrypt, "compare").mockResolvedValue(true);
    const signStub = jest.spyOn(jwt, "sign").mockReturnValue("token-palsu");
    const res = createMockResponse();

    // Act
    await loginUser({ body: { email: storedUser.email, password: "rahasia123" } }, res);

    // Assert
    expect(signStub.mock.calls[0][0]).toMatchObject({ role: "user", session_version: 0 });
  });

  test("LG-07: error database menghasilkan 500 - Stub error", async () => {
    // Arrange
    queryAsync.mockRejectedValueOnce(new Error("ECONNREFUSED"));
    const res = createMockResponse();

    // Act
    await loginUser({ body: { email: storedUser.email, password: "rahasia123" } }, res);

    // Assert
    expect(res.status).toHaveBeenCalledWith(500);
    expect(res.json).toHaveBeenCalledWith({
      success: false,
      message: "Terjadi kesalahan saat login",
    });
  });
});
