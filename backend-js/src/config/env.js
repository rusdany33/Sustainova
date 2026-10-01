const dotenv = require('dotenv');

dotenv.config({ path: require('path').resolve(__dirname, '../../.env') });

module.exports = {
    port: process.env.PORT,
    db: {
        host: process.env.DB_HOST,
        port: process.env.DB_PORT,
        user: process.env.DB_USER,
        password: process.env.DB_PASSWORD ?? process.env.DB_PASS ?? '',
        name: process.env.DB_NAME,
    },
    jwt: {
        secret: process.env.JWT_SECRET,
        expiresIn: process.env.JWT_EXPIRES_IN,
    },
}
