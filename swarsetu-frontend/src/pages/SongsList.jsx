import React, { useEffect, useState } from "react";
import API from "../api/api";
import { useNavigate } from "react-router-dom";

function SongsList() {

  const [songs, setSongs] = useState([]);
  const [title, setTitle] = useState("");

  const navigate = useNavigate();

  useEffect(() => {
    fetchSongs();
  }, []);

  const fetchSongs = async () => {
    const res = await API.get("songs/");
    setSongs(res.data);
  };

  const createSong = async () => {
    const res = await API.post("songs/", { title });
    navigate(`/editor/${res.data.id}`);
  };

  return (
    <div>

      <h2>Songs</h2>

      <input
        placeholder="Song title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      <button onClick={createSong}>Create Song</button>

      <hr />

      {songs.map(song => (
        <div key={song.id}>
          <b>{song.title}</b>

          <button onClick={() => navigate(`/editor/${song.id}`)}>
            Open
          </button>
        </div>
      ))}

    </div>
  );
}

export default SongsList;