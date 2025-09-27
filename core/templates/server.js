// --- 1. IMPORTS & SETUP (CommonJS) ---
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const multer = require('multer');
const path = require('path');

const app = express();
const PORT = 8000;
const API_BASE_URL = `http://localhost:${PORT}`;

// --- 2. MIDDLEWARE ---
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Serve static files from the 'uploads' directory
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

// --- 3. MONGODB DATABASE CONNECTION ---
const MONGO_URI = 'mongodb://localhost:27017/mannmitra';
mongoose.connect(MONGO_URI)
  .then(() => console.log('✅ Successfully connected to MongoDB!'))
  .catch(err => console.error('❌ Could not connect to MongoDB.', err));

// --- 4. MONGOOSE SCHEMAS & MODELS ---
const commentSchema = new mongoose.Schema({
    content: { type: String, required: true },
    pseudonym: { type: String, default: 'Anonymous' },
    post: { type: mongoose.Schema.Types.ObjectId, ref: 'Post', required: true }
}, { timestamps: true });

const Comment = mongoose.model('Comment', commentSchema);

const postSchema = new mongoose.Schema({
    title: { type: String, required: true },
    content: { type: String, required: true },
    pseudonym: { type: String, default: 'Anonymous' },
    category: { type: String, required: true },
    is_verified: { type: Boolean, default: false },
    is_anonymous: { type: Boolean, default: false },
    upvotes: { type: Number, default: 0 },
    comments_count: { type: Number, default: 0 },
    media_url: { type: String },
    tags: [String]
}, { timestamps: true });

const Post = mongoose.model('Post', postSchema);

// --- 5. FILE UPLOAD CONFIGURATION (Multer) ---
const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads/');
    },
    filename: (req, file, cb) => {
        const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1E9);
        cb(null, file.fieldname + '-' + uniqueSuffix + path.extname(file.originalname));
    }
});

const upload = multer({ storage: storage });

// --- 6. API ROUTES ---
app.get('/posts', async (req, res) => {
    try {
        const filter = {};
        if (req.query.category) filter.category = req.query.category;
        if (req.query.is_verified) filter.is_verified = req.query.is_verified;
        if (req.query.tag) filter.tags = req.query.tag;

        let query = Post.find(filter);

        if (req.query.sort === 'popular') {
            query = query.sort({ upvotes: -1 });
        } else {
            query = query.sort({ createdAt: -1 });
        }
        const posts = await query.exec();
        res.json(posts);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching posts', error });
    }
});

app.post('/posts', upload.single('media'), async (req, res) => {
    try {
        const { content, category, is_anonymous } = req.body;
        const title = content.split('.')[0] || "New Post";
        const newPost = new Post({
            title,
            content,
            category,
            is_anonymous: is_anonymous === 'true',
            pseudonym: is_anonymous === 'true' ? `User${Math.floor(Math.random() * 9000) + 1000}` : 'demo-user',
            tags: ['Motivation', 'StudyHelp']
        });
        if (req.file) {
            newPost.media_url = `${API_BASE_URL}/uploads/${req.file.filename}`;
        }
        await newPost.save();
        res.status(201).json(newPost);
    } catch (error) {
        res.status(500).json({ message: 'Error creating post', error: error.message });
    }
});

app.get('/posts/:postId/comments', async (req, res) => {
    try {
        const comments = await Comment.find({ post: req.params.postId }).sort({ createdAt: 'desc' });
        res.json(comments);
    } catch (error) {
        res.status(500).json({ message: 'Error fetching comments', error });
    }
});

app.post('/posts/:postId/comments', async (req, res) => {
    try {
        const newComment = new Comment({
            content: req.body.content,
            post: req.params.postId,
        });
        await newComment.save();
        await Post.findByIdAndUpdate(req.params.postId, { $inc: { comments_count: 1 } });
        res.status(201).json(newComment);
    } catch (error) {
        res.status(500).json({ message: 'Error posting comment', error });
    }
});

app.get('/leaderboard', (req, res) => {
    res.json([
        { pseudonym: 'Zenith_Peer', points: 245 },
        { pseudonym: 'Wellness_Seeker', points: 180 },
        { pseudonym: 'Happy_Fox_99', points: 150 },
    ]);
});

app.get('/trending', (req, res) => {
    res.json([
        { category: 'Anxiety', count: 1200 },
        { category: 'Exam Stress', count: 850 },
        { category: 'Relationships', count: 620 },
    ]);
});

// --- 7. START THE SERVER ---
app.listen(PORT, () => {
    console.log(`🚀 Server is running and listening on http://localhost:${PORT}`);
});