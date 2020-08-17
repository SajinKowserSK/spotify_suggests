import React from 'react';
import Player from './Player';
import Stars from './Stars';
import './App.css';
import ParticlesBg from "particles-bg";
import { Button, Divider, Image, Transition } from "semantic-ui-react";


class App extends React.Component {

  componentDidMount() {

    var headID = document.getElementsByTagName('head')[0];
        var link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.1/semantic.min.css'
        headID.appendChild(link);
  }



  state={
    song:"127QTOFJsJQp5LbJbu3A1y",
    visible: true,
    rating:0
  }


  print = () => {
    this.setState({song:'68UU9oaQtMDnh6PRlW842H'})
  }

  toggleVisibility = () =>{

  this.setState((prevState) => ({ visible: !prevState.visible }





    ))

    this.setState({song:'68UU9oaQtMDnh6PRlW842H'})

  }

  render()
  {
    const { visible } = this.state
  return (

<div>
<ParticlesBg color="#1DB954" type="circle" bg={true}/>


<div id="c"class="ui card">

        <div class="content">

          <div class="header">Toosie Slide - Drake</div>
          <div class="description">
          <Transition visible={visible} animation="pulse" duration={500}>
          <div>
            <Player song={this.state.song} />
            </div>
            </Transition>
          </div>

        </div>
        <div class="extra content">
          <center> Rate the song out of 5!</center>

            <Stars/>

          <center> <button onClick={this.toggleVisibility} class="positive ui button">Confirm Rating!</button></center>

        </div>


</div>

</div>

  );

}

}

export default App;
