import React from 'react';
import Player from './Player';
import Stars from './Stars';
import './App.css';

class App extends React.Component {

  state={
    song:"127QTOFJsJQp5LbJbu3A1y",
    rating:0
  }

  render()
  {
  return (

<div id="c"class="ui card">
  <div class="content">
  
    <div class="header">Toosie Slide - Drake</div>
    <div class="description">
      <Player song={this.state.song} />
    </div>
  </div>
   <div class="extra content">
    <center> Rate the song out of 5!</center> 
      <Stars/>

  </div>
 
</div>
  );

}

}

export default App;
