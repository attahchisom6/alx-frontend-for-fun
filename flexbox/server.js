const express = require('express');
const path = require('path');

const app = express();
const port = 5000;

const staticPath = path.join(__dirname, '');
console.log('The path is:', staticPath);

app.use(express.static(staticPath));

app.get('/:filename', (req, res) => {
  const filename = req.params.filename;
  console.log('This is filename:', filename);
  res.sendFile(path.join(staticPath, filename));
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on port ${port}`);
});
