import { useEffect, useState } from "react";
import API from "../api/api";

function Songs() {

  const [songs, setSongs] = useState([]);

  useEffect(() => {
    API.get("songs/")
      .then(res => setSongs(res.data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div>
      <h2>Songs</h2>

      {songs.map(song => (
        <div key={song.id}>
          <h3>{song.title}</h3>
        </div>
      ))}

    </div>
  );
}

export default Songs;