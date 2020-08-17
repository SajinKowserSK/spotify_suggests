import React from 'react';


const Player = (props) =>{
     var song =  "https://open.spotify.com/embed/track/" + props.song
    return(
        <iframe src={song} width="100%" 
        height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    )
}
export default Player;