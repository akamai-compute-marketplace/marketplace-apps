const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
    res.send("Hello from the Express backend!");
});

app.get("/api", (req, res) => {
    res.json({ message: "API is running!" });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
}); 