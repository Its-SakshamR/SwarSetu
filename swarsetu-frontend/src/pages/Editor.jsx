import React, { useEffect, useState } from "react";
import API from "../api/api";
import { useParams } from "react-router-dom";

function Editor() {

  const { songId } = useParams();

  const [lyrics,setLyrics] = useState("");
  const [translation,setTranslation] = useState("");

  useEffect(()=>{
    loadSong();
  },[]);

  const loadSong = async ()=>{

    const res = await API.get(`songs/${songId}/`);

    setLyrics(res.data.lyrics || "");
  };

  const save = async ()=>{

    await API.put(`songs/${songId}/`,{
      lyrics
    });

    alert("Saved");
  };

  const translate = async ()=>{

    const res = await API.post("translate/",{
      text: lyrics
    });

    setTranslation(res.data.translation);
  };

  return (
    <div>

      <h2>Song Editor</h2>

      <h3>English Lyrics</h3>

      <textarea
        rows="15"
        cols="80"
        value={lyrics}
        onChange={(e)=>setLyrics(e.target.value)}
      />

      <br/>

      <button onClick={save}>
        Save
      </button>

      <button onClick={translate}>
        Translate
      </button>

      <hr/>

      <h3>Hindi Translation</h3>

      <textarea
        rows="15"
        cols="80"
        value={translation}
        readOnly
      />

    </div>
  );
}

export default Editor;