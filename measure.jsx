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
        <Graph url="/fig/History_test2.svg" pollInterval="20000" id="graph1"/>
        <Device url="/api/devinfo" />
        <ConsumeInfo url="/api/consumehistory" pollInterval="20000"/>
        <Graph url="/fig/ConsumeInfo.svg" pollInterval="20000" id="graph2"/>
        <div clasName="clear"></div>
      </div>
    );
  }
});

ReactDOM.render(
  <Measure/>,
  document.getElementById('content')
);
