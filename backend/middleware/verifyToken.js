const jwt = require('jsonwebtoken');

const verifyToken = (req, res, next) => {
    // 1. Get the token from the Authorization header
    const bearerToken = req.headers.authorization;

    // 2. If no token is present, deny access
    if (!bearerToken) {
        return res.status(401).send({ message: "Unauthorized access. Please login to continue." });
    }

    // Extract the token from "Bearer <token>"
    const token = bearerToken.split(' ')[1];

    try {
        // 3. Verify the token
        const secret = process.env.JWT_SECRET || process.env.JWTT_SECRET;
        const decoded = jwt.verify(token, secret);
        // 4. Attach the decoded user payload to the request object
        req.user = decoded;
        // 5. Move to the next piece of middleware or the route handler
        next();
    } catch (err) {
        // If token is invalid or expired
        return res.status(401).send({ message: "Invalid or expired token." });
    }
};

module.exports = verifyToken;