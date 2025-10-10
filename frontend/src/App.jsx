import React, {useEffect, useState} from "react";
import axios from "axios";

export default function App(){
  const [posts, setPosts] = useState([]);
  const [form, setForm] = useState({account_id:1, content:"", media_url:"", scheduled_at:""});

  useEffect(()=>{ fetchPosts() },[]);

  async function fetchPosts(){
    const res = await axios.get("/api/posts/");
    setPosts(res.data);
  }

  async function submit(e){
    e.preventDefault();
    await axios.post("/api/posts/", form);
    setForm({...form, content:"", media_url:"", scheduled_at:""});
    fetchPosts();
  }

  return (
    <div style={{padding:20}}>
      <h2>Social Grow — Scheduler</h2>
      <form onSubmit={submit}>
        <div><input placeholder="Account ID" value={form.account_id} onChange={e=>setForm({...form, account_id: parseInt(e.target.value)})} /></div>
        <div><input placeholder="Media URL" value={form.media_url} onChange={e=>setForm({...form, media_url:e.target.value})} /></div>
        <div><input placeholder="Caption" value={form.content} onChange={e=>setForm({...form, content:e.target.value})} /></div>
        <div><input type="datetime-local" value={form.scheduled_at} onChange={e=>setForm({...form, scheduled_at:e.target.value})} /></div>
        <button type="submit">Schedule</button>
      </form>

      <h3>Scheduled posts</h3>
      <ul>
        {posts.map(p=>(
          <li key={p.id}>
            {p.id} — {p.content} — scheduled: {new Date(p.scheduled_at).toLocaleString()} — status: {p.status}
          </li>
        ))}
      </ul>
    </div>
  );
}
