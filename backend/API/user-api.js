const express = require('express')
const router = express.Router()
const bcrypt = require('bcryptjs')
const jwt = require('jsonwebtoken')

// POST /signup
// Body: { username, email, password }
router.post('/signup', async (req, res) => {
	try {
		const usersCollection = req.app.get('userscollection')
		if (!usersCollection) return res.status(500).json({ message: 'Database not initialized' })

		const { username, email, password } = req.body || {}
		if (!username || !email || !password) {
			return res.status(400).json({ message: 'Username, email and password are required' })
		}

		const emailRegex = /\S+@\S+\.\S+/
		if (!emailRegex.test(email)) {
			return res.status(400).json({ message: 'Invalid email address' })
		}

		// ensure username is unique (case-sensitive - use value as provided)
		const existing = await usersCollection.findOne({ username: username })
		if (existing) {
			return res.status(409).json({ message: 'Username already registered' })
		}

		const hashedPassword = bcrypt.hashSync(password, 10)

		const newUser = {
			username: username,
			email: email.toLowerCase(),
			password: hashedPassword
		}

		const result = await usersCollection.insertOne(newUser)

		return res.status(201).json({ message: 'User created', userId: result.insertedId })
	} catch (err) {
		console.error('Error in /signup:', err)
		return res.status(500).json({ message: 'Internal server error' })
	}
})

// POST /login
// Body: { username, password }
router.post('/login', async (req, res) => {
	try {
		const usersCollection = req.app.get('userscollection')
		if (!usersCollection) return res.status(500).json({ message: 'Database not initialized' })

		const { username, password } = req.body || {}
		if (!username || !password) return res.status(400).json({ message: 'Username and password are required' })

		const user = await usersCollection.findOne({ username: username })
		if (!user) return res.status(401).json({ message: 'Invalid username or password' })

		const match = await bcrypt.compare(password, user.password)
		if (!match) return res.status(401).json({ message: 'Invalid username or password' })

		// remove password before returning
		const { password: _p, ...userSafe } = user

		// sign JWT
		const payload = { userId: user._id.toString(), username: user.username }
		const secret = process.env.JWT_SECRET || process.env.JWTT_SECRET
		if (!secret) console.warn('JWT secret not set (checked JWT_SECRET and JWTT_SECRET) — using dev fallback secret')
		const token = jwt.sign(payload, secret, { expiresIn: '7d' })

		return res.json({ message: 'Login successful', token, user: userSafe })
	} catch (err) {
		console.error('Error in /login:', err)
		return res.status(500).json({ message: 'Internal server error' })
	}
})

module.exports = router

