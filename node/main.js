import { decode } from "./decode.js";
import express from 'express'
let app = express()
app.use(express.json()) // for parsing application/json

app.get('/', (req,res)=>{
    res.json({
        status: 'ready'
    })
})
app.post('/decode', (req,res)=>{
  req.body.data = JSON.parse(decode(req.body.data))
  res.json(req.body);
})

app.listen(1088)