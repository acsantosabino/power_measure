var React = require("react");
var Device = require("./templates/src/Device");
var Graph = require("./templates/src/Graph");
var MyTable = require("./templates/src/MyTable");
var ConsumeInfo = require("./templates/src/ConsumeInfo");

var Measure = React.createClass({
  render: function() {
    return (
      <div className="center">
        <MyTable title="History" url="/api/history" pollInterval="10000" />
        <Graph url="/fig/history.svg" pollInterval="20000">
          <a href="https://plot.ly/~TCC2016/0/" target="_blank" title="power_factor, current_mean, power_apparent, power_active, current_rms, voltage_rms, voltage_mean" style="display: block; text-align: center;"><img src="https://plot.ly/~TCC2016/0.png" alt="power_factor, current_mean, power_apparent, power_active, current_rms, voltage_rms, voltage_mean" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
          <script data-plotly="TCC2016:0"  src="https://plot.ly/embed.js" async></script>
        <Graph/>
        <Device url="/api/devinfo" />
        <ConsumeInfo url="/api/consumehistory" pollInterval="20000"/>
        <Graph url="/fig/history.svg" pollInterval="20000">
          <a href="https://plot.ly/~TCC2016/0/" target="_blank" title="power_factor, current_mean, power_apparent, power_active, current_rms, voltage_rms, voltage_mean" style="display: block; text-align: center;"><img src="https://plot.ly/~TCC2016/0.png" alt="power_factor, current_mean, power_apparent, power_active, current_rms, voltage_rms, voltage_mean" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
          <script 
        <div clasName="clear"></div>
      </div>
    );
  }
});

ReactDOM.render(
  <Measure/>,
  document.getElementById('content')
);
