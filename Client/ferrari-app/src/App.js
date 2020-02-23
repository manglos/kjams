import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  function onPauseClick() {
    fetch("http://localhost:8978/pause", {
      method: "POST"
    })
    .then(response=>response.json());
  }

  function onNextClick() {
    fetch("http://localhost:8978/next", {
      method: "POST"
    })
    .then(response=>response.json());
  }

  function onPreviousClick() {
    fetch("http://localhost:8978/previous", {
      method: "POST"
    })
    .then(response=>response.json());
  }

  function onStopClick() {
    fetch("http://localhost:8978/stop", {
      method: "POST"
    })
    .then(response=>response.json());
  }

  function onVolumeUpClick() {
    fetch("http://localhost:8978/volume-up", {
      method: "POST"
    })
    .then(response=>response.json());
  }

  function onVolumeDownClick() {
    fetch("http://localhost:8978/volume-down", {
      method: "POST"
    })
    .then(response=>response.json());
  }


  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <span>
        <button
          onClick={onPreviousClick}>
          Previous
        </button>
        </span>
        <span>
        <button
          onClick={onPauseClick}>
          Pause
        </button>
        </span>
        <span>
        <button
          onClick={onStopClick}>
          Stop
        </button>
        </span>
        <span>
        <button
          onClick={onNextClick}>
          Next
        </button>
        </span>
        <span>
        <button
          onClick={onVolumeUpClick}>
          +
        </button>
        </span>
        <span>
        <button
          onClick={onVolumeDownClick}>
          -
        </button>
        </span>
      </header>
    </div>
  );
}

export default App;
