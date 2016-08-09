!function(m){"object"==typeof module&&module.exports?module.exports=m:m(Highcharts)}(function(m){function M(a,b,c){this.init(a,b,c)}var R=m.arrayMin,S=m.arrayMax,t=m.each,H=m.extend,I=m.isNumber,u=m.merge,T=m.map,o=m.pick,B=m.pInt,G=m.correctFloat,p=m.getOptions().plotOptions,i=m.seriesTypes,v=m.extendClass,N=m.splat,w=m.wrap,O=m.Axis,z=m.Tick,J=m.Point,U=m.Pointer,V=m.CenteredSeriesMixin,C=m.TrackerMixin,x=m.Series,y=Math,F=y.round,D=y.floor,P=y.max,W=m.Color,r=function(){};H(M.prototype,{init:function(a,b,c){var d=this,g=d.defaultOptions;d.chart=b,d.options=a=u(g,b.angular?{background:{}}:void 0,a),(a=a.background)&&t([].concat(N(a)).reverse(),function(a){var b=a.backgroundColor,g=c.userOptions,a=u(d.defaultBackgroundOptions,a);b&&(a.backgroundColor=b),a.color=a.backgroundColor,c.options.plotBands.unshift(a),g.plotBands=g.plotBands||[],g.plotBands!==c.options.plotBands&&g.plotBands.unshift(a)})},defaultOptions:{center:["50%","50%"],size:"85%",startAngle:0},defaultBackgroundOptions:{shape:"circle",borderWidth:1,borderColor:"silver",backgroundColor:{linearGradient:{x1:0,y1:0,x2:0,y2:1},stops:[[0,"#FFF"],[1,"#DDD"]]},from:-Number.MAX_VALUE,innerRadius:0,to:Number.MAX_VALUE,outerRadius:"105%"}});var A=O.prototype,z=z.prototype,X={getOffset:r,redraw:function(){this.isDirty=!1},render:function(){this.isDirty=!1},setScale:r,setCategories:r,setTitle:r},Q={isRadial:!0,defaultRadialGaugeOptions:{labels:{align:"center",x:0,y:null},minorGridLineWidth:0,minorTickInterval:"auto",minorTickLength:10,minorTickPosition:"inside",minorTickWidth:1,tickLength:10,tickPosition:"inside",tickWidth:2,title:{rotation:0},zIndex:2},defaultRadialXOptions:{gridLineWidth:1,labels:{align:null,distance:15,x:0,y:null},maxPadding:0,minPadding:0,showLastLabel:!1,tickLength:0},defaultRadialYOptions:{gridLineInterpolation:"circle",labels:{align:"right",x:-3,y:-2},showLastLabel:!1,title:{x:4,text:null,rotation:90}},setOptions:function(a){a=this.options=u(this.defaultOptions,this.defaultRadialOptions,a),a.plotBands||(a.plotBands=[])},getOffset:function(){A.getOffset.call(this),this.chart.axisOffset[this.side]=0,this.center=this.pane.center=V.getCenter.call(this.pane)},getLinePath:function(a,b){var c=this.center,b=o(b,c[2]/2-this.offset);return this.chart.renderer.symbols.arc(this.left+c[0],this.top+c[1],b,b,{start:this.startAngleRad,end:this.endAngleRad,open:!0,innerR:0})},setAxisTranslation:function(){A.setAxisTranslation.call(this),this.center&&(this.transA=this.isCircular?(this.endAngleRad-this.startAngleRad)/(this.max-this.min||1):this.center[2]/2/(this.max-this.min||1),this.minPixelPadding=this.isXAxis?this.transA*this.minPointOffset:0)},beforeSetTickPositions:function(){this.autoConnect&&(this.max+=this.categories&&1||this.pointRange||this.closestPointRange||0)},setAxisSize:function(){A.setAxisSize.call(this),this.isRadial&&(this.center=this.pane.center=m.CenteredSeriesMixin.getCenter.call(this.pane),this.isCircular&&(this.sector=this.endAngleRad-this.startAngleRad),this.len=this.width=this.height=this.center[2]*o(this.sector,1)/2)},getPosition:function(a,b){return this.postTranslate(this.isCircular?this.translate(a):0,o(this.isCircular?b:this.translate(a),this.center[2]/2)-this.offset)},postTranslate:function(a,b){var c=this.chart,d=this.center,a=this.startAngleRad+a;return{x:c.plotLeft+d[0]+Math.cos(a)*b,y:c.plotTop+d[1]+Math.sin(a)*b}},getPlotBandPath:function(a,b,c){var h,d=this.center,g=this.startAngleRad,e=d[2]/2,j=[o(c.outerRadius,"100%"),c.innerRadius,o(c.thickness,10)],l=/%$/,f=this.isCircular;return"polygon"===this.options.gridLineInterpolation?d=this.getPlotLinePath(a).concat(this.getPlotLinePath(b,!0)):(a=Math.max(a,this.min),b=Math.min(b,this.max),f||(j[0]=this.translate(a),j[1]=this.translate(b)),j=T(j,function(a){return l.test(a)&&(a=B(a,10)*e/100),a}),"circle"!==c.shape&&f?(a=g+this.translate(a),b=g+this.translate(b)):(a=-Math.PI/2,b=1.5*Math.PI,h=!0),d=this.chart.renderer.symbols.arc(this.left+d[0],this.top+d[1],j[0],j[0],{start:Math.min(a,b),end:Math.max(a,b),innerR:o(j[1],j[0]-j[2]),open:h})),d},getPlotLinePath:function(a,b){var j,l,h,c=this,d=c.center,g=c.chart,e=c.getPosition(a);return c.isCircular?h=["M",d[0]+g.plotLeft,d[1]+g.plotTop,"L",e.x,e.y]:"circle"===c.options.gridLineInterpolation?(a=c.translate(a))&&(h=c.getLinePath(0,a)):(t(g.xAxis,function(a){a.pane===c.pane&&(j=a)}),h=[],a=c.translate(a),d=j.tickPositions,j.autoConnect&&(d=d.concat([d[0]])),b&&(d=[].concat(d).reverse()),t(d,function(e,b){l=j.getPosition(e,a),h.push(b?"L":"M",l.x,l.y)})),h},getTitlePosition:function(){var a=this.center,b=this.chart,c=this.options.title;return{x:b.plotLeft+a[0]+(c.x||0),y:b.plotTop+a[1]-{high:.5,middle:.25,low:0}[c.align]*a[2]+(c.y||0)}}};w(A,"init",function(a,b,c){var k,l,h,d=b.angular,g=b.polar,e=c.isX,j=d&&e;h=b.options;var f=c.pane||0;d?(H(this,j?X:Q),(l=!e)&&(this.defaultRadialOptions=this.defaultRadialGaugeOptions)):g&&(H(this,Q),this.defaultRadialOptions=(l=e)?this.defaultRadialXOptions:u(this.defaultYAxisOptions,this.defaultRadialYOptions)),(d||g)&&(b.inverted=!1,h.chart.zoomType=null),a.call(this,b,c),j||!d&&!g||(a=this.options,b.panes||(b.panes=[]),this.pane=(k=b.panes[f]=b.panes[f]||new M(N(h.pane)[f],b,this),b=k),h=b.options,this.startAngleRad=b=(h.startAngle-90)*Math.PI/180,this.endAngleRad=h=(o(h.endAngle,h.startAngle+360)-90)*Math.PI/180,this.offset=a.offset||0,(this.isCircular=l)&&void 0===c.max&&h-b===2*Math.PI&&(this.autoConnect=!0))}),w(A,"autoLabelAlign",function(a){return this.isRadial?void 0:a.apply(this,[].slice.call(arguments,1))}),w(z,"getPosition",function(a,b,c,d,g){var e=this.axis;return e.getPosition?e.getPosition(c):a.call(this,b,c,d,g)}),w(z,"getLabelPosition",function(a,b,c,d,g,e,j,l,h){var f=this.axis,k=e.y,n=20,s=e.align,i=(f.translate(this.pos)+f.startAngleRad+Math.PI/2)/Math.PI*180%360;return f.isRadial?(a=f.getPosition(this.pos,f.center[2]/2+o(e.distance,-25)),"auto"===e.rotation?d.attr({rotation:i}):null===k&&(k=f.chart.renderer.fontMetrics(d.styles.fontSize).b-d.getBBox().height/2),null===s&&(f.isCircular?(this.label.getBBox().width>f.len*f.tickInterval/(f.max-f.min)&&(n=0),s=i>n&&180-n>i?"left":i>180+n&&360-n>i?"right":"center"):s="center",d.attr({align:s})),a.x+=e.x,a.y+=k):a=a.call(this,b,c,d,g,e,j,l,h),a}),w(z,"getMarkPath",function(a,b,c,d,g,e,j){var l=this.axis;return l.isRadial?(a=l.getPosition(this.pos,l.center[2]/2+d),b=["M",b,c,"L",a.x,a.y]):b=a.call(this,b,c,d,g,e,j),b}),p.arearange=u(p.area,{lineWidth:1,marker:null,threshold:null,tooltip:{pointFormat:'<span style="color:{series.color}">●</span> {series.name}: <b>{point.low}</b> - <b>{point.high}</b><br/>'},trackByArea:!0,dataLabels:{align:null,verticalAlign:null,xLow:0,xHigh:0,yLow:0,yHigh:0},states:{hover:{halo:!1}}}),i.arearange=v(i.area,{type:"arearange",pointArrayMap:["low","high"],dataLabelCollections:["dataLabel","dataLabelUpper"],toYData:function(a){return[a.low,a.high]},pointValKey:"low",deferTranslatePolar:!0,highToXY:function(a){var b=this.chart,c=this.xAxis.postTranslate(a.rectPlotX,this.yAxis.len-a.plotHigh);a.plotHighX=c.x-b.plotLeft,a.plotHigh=c.y-b.plotTop},translate:function(){var a=this,b=a.yAxis;i.area.prototype.translate.apply(a),t(a.points,function(a){var d=a.low,g=a.high,e=a.plotY;null===g||null===d?a.isNull=!0:(a.plotLow=e,a.plotHigh=b.translate(g,0,1,0,1))}),this.chart.polar&&t(this.points,function(b){a.highToXY(b)})},getGraphPath:function(){var e,j,l,a=this.points,b=[],c=[],d=a.length,g=x.prototype.getGraphPath;l=this.options;for(var h=l.step,d=a.length;d--;)e=a[d],!e.isNull&&(!a[d+1]||a[d+1].isNull)&&c.push({plotX:e.plotX,plotY:e.plotLow}),j={plotX:e.plotX,plotY:e.plotHigh,isNull:e.isNull},c.push(j),b.push(j),!e.isNull&&(!a[d-1]||a[d-1].isNull)&&c.push({plotX:e.plotX,plotY:e.plotLow});return a=g.call(this,a),h&&(h===!0&&(h="left"),l.step={left:"right",center:"center",right:"left"}[h]),b=g.call(this,b),c=g.call(this,c),l.step=h,l=[].concat(a,b),!this.chart.polar&&"M"===c[0]&&(c[0]="L"),this.areaPath=this.areaPath.concat(a,c),l},drawDataLabels:function(){var c,f,k,a=this.data,b=a.length,d=[],g=x.prototype,e=this.options.dataLabels,j=e.align,l=e.verticalAlign,h=e.inside,n=this.chart.inverted;if(e.enabled||this._hasPointLabels){for(c=b;c--;)(f=a[c])&&(k=h?f.plotHigh<f.plotLow:f.plotHigh>f.plotLow,f.y=f.high,f._plotY=f.plotY,f.plotY=f.plotHigh,d[c]=f.dataLabel,f.dataLabel=f.dataLabelUpper,f.below=k,n?j||(e.align=k?"right":"left"):l||(e.verticalAlign=k?"top":"bottom"),e.x=e.xHigh,e.y=e.yHigh);for(g.drawDataLabels&&g.drawDataLabels.apply(this,arguments),c=b;c--;)(f=a[c])&&(k=h?f.plotHigh<f.plotLow:f.plotHigh>f.plotLow,f.dataLabelUpper=f.dataLabel,f.dataLabel=d[c],f.y=f.low,f.plotY=f._plotY,f.below=!k,n?j||(e.align=k?"left":"right"):l||(e.verticalAlign=k?"bottom":"top"),e.x=e.xLow,e.y=e.yLow);g.drawDataLabels&&g.drawDataLabels.apply(this,arguments)}e.align=j,e.verticalAlign=l},alignDataLabel:function(){i.column.prototype.alignDataLabel.apply(this,arguments)},setStackedPoints:r,getSymbol:r,drawPoints:r}),p.areasplinerange=u(p.arearange),i.areasplinerange=v(i.arearange,{type:"areasplinerange",getPointSpline:i.spline.prototype.getPointSpline}),function(){var a=i.column.prototype;p.columnrange=u(p.column,p.arearange,{lineWidth:1,pointRange:null}),i.columnrange=v(i.arearange,{type:"columnrange",translate:function(){var e,h,b=this,c=b.yAxis,d=b.xAxis,g=d.startAngleRad,j=b.chart,l=b.xAxis.isRadial;a.translate.apply(b),t(b.points,function(a){var s,i,k=a.shapeArgs,n=b.options.minPointLength;a.plotHigh=h=c.translate(a.high,0,1,0,1),a.plotLow=a.plotY,i=h,s=o(a.rectPlotY,a.plotY)-h,Math.abs(s)<n?(n-=s,s+=n,i-=n/2):0>s&&(s*=-1,i-=s),l?(e=a.barX+g,a.shapeType="path",a.shapeArgs={d:b.polarArc(i+s,i,e,e+a.pointWidth)}):(k.height=s,k.y=i,a.tooltipPos=j.inverted?[c.len+c.pos-j.plotLeft-i-s/2,d.len+d.pos-j.plotTop-k.x-k.width/2,s]:[d.left-j.plotLeft+k.x+k.width/2,c.pos-j.plotTop+i+s/2,s])})},directTouch:!0,trackerGroups:["group","dataLabelsGroup"],drawGraph:r,crispCol:a.crispCol,pointAttrToOptions:a.pointAttrToOptions,drawPoints:a.drawPoints,drawTracker:a.drawTracker,getColumnMetrics:a.getColumnMetrics,animate:function(){return a.animate.apply(this,arguments)},polarArc:function(){return a.polarArc.apply(this,arguments)}})}(),p.gauge=u(p.line,{dataLabels:{enabled:!0,defer:!1,y:15,borderWidth:1,borderColor:"silver",borderRadius:3,crop:!1,verticalAlign:"top",zIndex:2},dial:{},pivot:{},tooltip:{headerFormat:""},showInLegend:!1}),C={type:"gauge",pointClass:v(J,{setState:function(a){this.state=a}}),angular:!0,directTouch:!0,drawGraph:r,fixedBox:!0,forceDL:!0,trackerGroups:["group","dataLabelsGroup"],translate:function(){var a=this.yAxis,b=this.options,c=a.center;this.generatePoints(),t(this.points,function(d){var g=u(b.dial,d.dial),e=B(o(g.radius,80))*c[2]/200,j=B(o(g.baseLength,70))*e/100,l=B(o(g.rearLength,10))*e/100,h=g.baseWidth||3,f=g.topWidth||1,k=b.overshoot,n=a.startAngleRad+a.translate(d.y,null,null,null,!0);I(k)?(k=k/180*Math.PI,n=Math.max(a.startAngleRad-k,Math.min(a.endAngleRad+k,n))):b.wrap===!1&&(n=Math.max(a.startAngleRad,Math.min(a.endAngleRad,n))),n=180*n/Math.PI,d.shapeType="path",d.shapeArgs={d:g.path||["M",-l,-h/2,"L",j,-h/2,e,-f/2,e,f/2,j,h/2,-l,h/2,"z"],translateX:c[0],translateY:c[1],rotation:n},d.plotX=c[0],d.plotY=c[1]})},drawPoints:function(){var a=this,b=a.yAxis.center,c=a.pivot,d=a.options,g=d.pivot,e=a.chart.renderer;t(a.points,function(b){var g=b.graphic,c=b.shapeArgs,f=c.d,k=u(d.dial,b.dial);g?(g.animate(c),c.d=f):b.graphic=e[b.shapeType](c).attr({stroke:k.borderColor||"none","stroke-width":k.borderWidth||0,fill:k.backgroundColor||"black",rotation:c.rotation,zIndex:1}).add(a.group)}),c?c.animate({translateX:b[0],translateY:b[1]}):a.pivot=e.circle(0,0,o(g.radius,5)).attr({"stroke-width":g.borderWidth||0,stroke:g.borderColor||"silver",fill:g.backgroundColor||"black",zIndex:2}).translate(b[0],b[1]).add(a.group)},animate:function(a){var b=this;a||(t(b.points,function(a){var d=a.graphic;d&&(d.attr({rotation:180*b.yAxis.startAngleRad/Math.PI}),d.animate({rotation:a.shapeArgs.rotation},b.options.animation))}),b.animate=null)},render:function(){this.group=this.plotGroup("group","series",this.visible?"visible":"hidden",this.options.zIndex,this.chart.seriesGroup),x.prototype.render.call(this),this.group.clip(this.chart.clipRect)},setData:function(a,b){x.prototype.setData.call(this,a,!1),this.processData(),this.generatePoints(),o(b,!0)&&this.chart.redraw()},drawTracker:C&&C.drawTrackerPoint},i.gauge=v(i.line,C),p.boxplot=u(p.column,{fillColor:"#FFFFFF",lineWidth:1,medianWidth:2,states:{hover:{brightness:-.3}},threshold:null,tooltip:{pointFormat:'<span style="color:{point.color}">●</span> <b> {series.name}</b><br/>Maximum: {point.high}<br/>Upper quartile: {point.q3}<br/>Median: {point.median}<br/>Lower quartile: {point.q1}<br/>Minimum: {point.low}<br/>'},whiskerLength:"50%",whiskerWidth:2}),i.boxplot=v(i.column,{type:"boxplot",pointArrayMap:["low","q1","median","q3","high"],toYData:function(a){return[a.low,a.q1,a.median,a.q3,a.high]},pointValKey:"high",pointAttrToOptions:{fill:"fillColor",stroke:"color","stroke-width":"lineWidth"},drawDataLabels:r,translate:function(){var a=this.yAxis,b=this.pointArrayMap;i.column.prototype.translate.apply(this),t(this.points,function(c){t(b,function(b){null!==c[b]&&(c[b+"Plot"]=a.translate(c[b],0,1,0,1))})})},drawPoints:function(){var d,g,e,j,l,h,f,k,n,i,m,K,L,p,u,r,w,v,x,y,C,B,A,a=this,b=a.options,c=a.chart.renderer,z=a.doQuartiles!==!1,E=a.options.whiskerLength;t(a.points,function(q){n=q.graphic,C=q.shapeArgs,m={},p={},r={},B=q.color||a.color,void 0!==q.plotY&&(d=q.pointAttr[q.selected?"selected":""],w=C.width,v=D(C.x),x=v+w,y=F(w/2),g=D(z?q.q1Plot:q.lowPlot),e=D(z?q.q3Plot:q.lowPlot),j=D(q.highPlot),l=D(q.lowPlot),m.stroke=q.stemColor||b.stemColor||B,m["stroke-width"]=o(q.stemWidth,b.stemWidth,b.lineWidth),m.dashstyle=q.stemDashStyle||b.stemDashStyle,p.stroke=q.whiskerColor||b.whiskerColor||B,p["stroke-width"]=o(q.whiskerWidth,b.whiskerWidth,b.lineWidth),r.stroke=q.medianColor||b.medianColor||B,r["stroke-width"]=o(q.medianWidth,b.medianWidth,b.lineWidth),f=m["stroke-width"]%2/2,k=v+y+f,i=["M",k,e,"L",k,j,"M",k,g,"L",k,l],z&&(f=d["stroke-width"]%2/2,k=D(k)+f,g=D(g)+f,e=D(e)+f,v+=f,x+=f,K=["M",v,e,"L",v,g,"L",x,g,"L",x,e,"L",v,e,"z"]),E&&(f=p["stroke-width"]%2/2,j+=f,l+=f,A=/%$/.test(E)?y*parseFloat(E)/100:E/2,L=["M",k-A,j,"L",k+A,j,"M",k-A,l,"L",k+A,l]),f=r["stroke-width"]%2/2,h=F(q.medianPlot)+f,u=["M",v,h,"L",x,h],n?(q.stem.animate({d:i}),E&&q.whiskers.animate({d:L}),z&&q.box.animate({d:K}),q.medianShape.animate({d:u})):(q.graphic=n=c.g().add(a.group),q.stem=c.path(i).attr(m).add(n),E&&(q.whiskers=c.path(L).attr(p).add(n)),z&&(q.box=c.path(K).attr(d).add(n)),q.medianShape=c.path(u).attr(r).add(n)))})},setStackedPoints:r}),p.errorbar=u(p.boxplot,{color:"#000000",grouping:!1,linkedTo:":previous",tooltip:{pointFormat:'<span style="color:{point.color}">●</span> {series.name}: <b>{point.low}</b> - <b>{point.high}</b><br/>'},whiskerWidth:null}),i.errorbar=v(i.boxplot,{type:"errorbar",pointArrayMap:["low","high"],toYData:function(a){return[a.low,a.high]},pointValKey:"high",doQuartiles:!1,drawDataLabels:i.arearange?i.arearange.prototype.drawDataLabels:r,getColumnMetrics:function(){return this.linkedParent&&this.linkedParent.columnMetrics||i.column.prototype.getColumnMetrics.call(this)}}),p.waterfall=u(p.column,{lineWidth:1,lineColor:"#333",dashStyle:"dot",borderColor:"#333",dataLabels:{inside:!0},states:{hover:{lineWidthPlus:0}}}),i.waterfall=v(i.column,{type:"waterfall",upColorProp:"fill",pointValKey:"y",translate:function(){var c,d,g,e,j,l,h,f,k,a=this.options,b=this.yAxis,n=o(a.minPointLength,5),s=a.threshold,m=a.stacking;for(i.column.prototype.translate.apply(this),this.minPointLengthOffset=0,h=f=s,d=this.points,c=0,a=d.length;a>c;c++)g=d[c],l=this.processedYData[c],e=g.shapeArgs,k=(j=m&&b.stacks[(this.negStacks&&s>l?"-":"")+this.stackKey])?j[g.x].points[this.index+","+c]:[0,l],g.isSum?g.y=G(l):g.isIntermediateSum&&(g.y=G(l-f)),j=P(h,h+g.y)+k[0],e.y=b.translate(j,0,1),g.isSum?(e.y=b.translate(k[1],0,1),e.height=Math.min(b.translate(k[0],0,1),b.len)-e.y+this.minPointLengthOffset):g.isIntermediateSum?(e.y=b.translate(k[1],0,1),e.height=Math.min(b.translate(f,0,1),b.len)-e.y+this.minPointLengthOffset,f=k[1]):(0!==h&&(e.height=l>0?b.translate(h,0,1)-e.y:b.translate(h,0,1)-b.translate(h-l,0,1)),h+=l),e.height<0&&(e.y+=e.height,e.height*=-1),g.plotY=e.y=F(e.y)-this.borderWidth%2/2,e.height=P(F(e.height),.001),g.yBottom=e.y+e.height,e.height<=n&&(e.height=n,this.minPointLengthOffset+=n),e.y-=this.minPointLengthOffset,e=g.plotY+(g.negative?e.height:0)-this.minPointLengthOffset,this.chart.inverted?g.tooltipPos[0]=b.len-e:g.tooltipPos[1]=e},processData:function(a){var d,e,j,l,h,f,k,b=this.yData,c=this.options.data,g=b.length;for(j=e=l=h=this.options.threshold||0,k=0;g>k;k++)f=b[k],d=c&&c[k]?c[k]:{},"sum"===f||d.isSum?b[k]=G(j):"intermediateSum"===f||d.isIntermediateSum?b[k]=G(e):(j+=f,e+=f),l=Math.min(j,l),h=Math.max(j,h);x.prototype.processData.call(this,a),this.dataMin=l,this.dataMax=h},toYData:function(a){return a.isSum?0===a.x?null:"sum":a.isIntermediateSum?0===a.x?null:"intermediateSum":a.y},getAttribs:function(){i.column.prototype.getAttribs.apply(this,arguments);var a=this,b=a.options,c=b.states,d=b.upColor||a.color,b=m.Color(d).brighten(.1).get(),g=u(a.pointAttr),e=a.upColorProp;g[""][e]=d,g.hover[e]=c.hover.upColor||b,g.select[e]=c.select.upColor||d,t(a.points,function(e){e.options.color||(e.y>0?(e.pointAttr=g,e.color=d):e.pointAttr=a.pointAttr)})},getGraphPath:function(){var g,e,j,a=this.data,b=a.length,c=F(this.options.lineWidth+this.borderWidth)%2/2,d=[];for(j=1;b>j;j++)e=a[j].shapeArgs,g=a[j-1].shapeArgs,e=["M",g.x+g.width,g.y+c,"L",e.x,g.y+c],a[j-1].y<0&&(e[2]+=g.height,e[5]+=g.height),d=d.concat(e);return d},getExtremes:r,drawGraph:x.prototype.drawGraph}),p.polygon=u(p.scatter,{marker:{enabled:!1}}),i.polygon=v(i.scatter,{type:"polygon",fillGraph:!0,getSegmentPath:function(a){return x.prototype.getSegmentPath.call(this,a).concat("z")},drawGraph:x.prototype.drawGraph,drawLegendSymbol:m.LegendSymbolMixin.drawRectangle}),p.bubble=u(p.scatter,{dataLabels:{formatter:function(){return this.point.z},inside:!0,verticalAlign:"middle"},marker:{lineColor:null,lineWidth:1},minSize:8,maxSize:"20%",softThreshold:!1,states:{hover:{halo:{size:5}}},tooltip:{pointFormat:"({point.x}, {point.y}), Size: {point.z}"},turboThreshold:0,zThreshold:0,zoneAxis:"z"}),C=v(J,{haloPath:function(){return J.prototype.haloPath.call(this,this.shapeArgs.r+this.series.options.states.hover.halo.size)},ttBelow:!1}),i.bubble=v(i.scatter,{type:"bubble",pointClass:C,pointArrayMap:["y","z"],parallelArrays:["x","y","z"],trackerGroups:["group","dataLabelsGroup"],bubblePadding:!0,zoneAxis:"z",pointAttrToOptions:{stroke:"lineColor","stroke-width":"lineWidth",fill:"fillColor"},applyOpacity:function(a){var b=this.options.marker,c=o(b.fillOpacity,.5),a=a||b.fillColor||this.color;return 1!==c&&(a=W(a).setOpacity(c).get("rgba")),a},convertAttribs:function(){var a=x.prototype.convertAttribs.apply(this,arguments);return a.fill=this.applyOpacity(a.fill),a},getRadii:function(a,b,c,d){var g,e,j,l=this.zData,h=[],f=this.options,k="width"!==f.sizeBy,n=f.zThreshold,i=b-a;for(e=0,g=l.length;g>e;e++)j=l[e],f.sizeByAbsoluteValue&&null!==j&&(j=Math.abs(j-n),b=Math.max(b-n,Math.abs(a-n)),a=0),null===j?j=null:a>j?j=c/2-1:(j=i>0?(j-a)/i:.5,k&&j>=0&&(j=Math.sqrt(j)),j=y.ceil(c+j*(d-c))/2),h.push(j);this.radii=h},animate:function(a){var b=this.options.animation;a||(t(this.points,function(a){var d=a.graphic,a=a.shapeArgs;d&&a&&(d.attr("r",1),d.animate({r:a.r},b))}),this.animate=null)},translate:function(){var a,c,d,b=this.data,g=this.radii;for(i.scatter.prototype.translate.call(this),a=b.length;a--;)c=b[a],d=g?g[a]:0,I(d)&&d>=this.minPxSize/2?(c.shapeType="circle",c.shapeArgs={x:c.plotX,y:c.plotY,r:d},c.dlBox={x:c.plotX-d,y:c.plotY-d,width:2*d,height:2*d}):c.shapeArgs=c.plotY=c.dlBox=void 0},drawLegendSymbol:function(a,b){var c=this.chart.renderer,d=c.fontMetrics(a.itemStyle.fontSize).f/2;b.legendSymbol=c.circle(d,a.baseline-d,d).attr({zIndex:3}).add(b.legendGroup),b.legendSymbol.isMarker=!0},drawPoints:i.column.prototype.drawPoints,alignDataLabel:i.column.prototype.alignDataLabel,buildKDTree:r,applyZones:r}),O.prototype.beforePadding=function(){var a=this,b=this.len,c=this.chart,d=0,g=b,e=this.isXAxis,j=e?"xData":"yData",l=this.min,h={},f=y.min(c.plotWidth,c.plotHeight),k=Number.MAX_VALUE,n=-Number.MAX_VALUE,i=this.max-l,m=b/i,p=[];t(this.series,function(b){var g=b.options;!b.bubblePadding||!b.visible&&c.options.chart.ignoreHiddenSeries||(a.allowZoomOutside=!0,p.push(b),e&&(t(["minSize","maxSize"],function(a){var b=g[a],e=/%$/.test(b),b=B(b);h[a]=e?f*b/100:b}),b.minPxSize=h.minSize,b.maxPxSize=h.maxSize,b=b.zData,b.length&&(k=o(g.zMin,y.min(k,y.max(R(b),g.displayNegative===!1?g.zThreshold:-Number.MAX_VALUE))),n=o(g.zMax,y.max(n,S(b))))))}),t(p,function(b){var h,c=b[j],f=c.length;if(e&&b.getRadii(k,n,b.minPxSize,b.maxPxSize),i>0)for(;f--;)I(c[f])&&a.dataMin<=c[f]&&c[f]<=a.dataMax&&(h=b.radii[f],d=Math.min((c[f]-l)*m-h,d),g=Math.max((c[f]-l)*m+h,g))}),p.length&&i>0&&!this.isLog&&(g-=b,m*=(b+d-g)/b,t([["min","userMin",d],["max","userMax",g]],function(b){void 0===o(a.options[b[0]],a[b[1]])&&(a[b[0]]+=b[2]/m)}))},function(){function a(a,b){var c=this.chart,d=this.options.animation,h=this.group,f=this.markerGroup,k=this.xAxis.center,i=c.plotLeft,m=c.plotTop;c.polar?c.renderer.isSVG&&(d===!0&&(d={}),b?(c={translateX:k[0]+i,translateY:k[1]+m,scaleX:.001,scaleY:.001},h.attr(c),f&&f.attr(c)):(c={translateX:i,translateY:m,scaleX:1,scaleY:1},h.animate(c,d),f&&f.animate(c,d),this.animate=null)):a.call(this,b)}var d,b=x.prototype,c=U.prototype;b.searchPointByAngle=function(a){var b=this.chart,c=this.xAxis.pane.center;return this.searchKDTree({clientX:180+Math.atan2(a.chartX-c[0]-b.plotLeft,a.chartY-c[1]-b.plotTop)*(-180/Math.PI)})},w(b,"buildKDTree",function(a){this.chart.polar&&(this.kdByAngle?this.searchPoint=this.searchPointByAngle:this.kdDimensions=2),a.apply(this)}),b.toXY=function(a){var b,c=this.chart,d=a.plotX;b=a.plotY,a.rectPlotX=d,a.rectPlotY=b,b=this.xAxis.postTranslate(a.plotX,this.yAxis.len-b),a.plotX=a.polarPlotX=b.x-c.plotLeft,a.plotY=a.polarPlotY=b.y-c.plotTop,this.kdByAngle?(c=(d/Math.PI*180+this.xAxis.pane.options.startAngle)%360,0>c&&(c+=360),a.clientX=c):a.clientX=a.plotX},i.spline&&w(i.spline.prototype,"getPointSpline",function(a,b,c,d){var h,f,k,i,m,p,o;return this.chart.polar?(h=c.plotX,f=c.plotY,a=b[d-1],k=b[d+1],this.connectEnds&&(a||(a=b[b.length-2]),k||(k=b[1])),a&&k&&(i=a.plotX,m=a.plotY,b=k.plotX,p=k.plotY,i=(1.5*h+i)/2.5,m=(1.5*f+m)/2.5,k=(1.5*h+b)/2.5,o=(1.5*f+p)/2.5,b=Math.sqrt(Math.pow(i-h,2)+Math.pow(m-f,2)),p=Math.sqrt(Math.pow(k-h,2)+Math.pow(o-f,2)),i=Math.atan2(m-f,i-h),m=Math.atan2(o-f,k-h),o=Math.PI/2+(i+m)/2,Math.abs(i-o)>Math.PI/2&&(o-=Math.PI),i=h+Math.cos(o)*b,m=f+Math.sin(o)*b,k=h+Math.cos(Math.PI+o)*p,o=f+Math.sin(Math.PI+o)*p,c.rightContX=k,c.rightContY=o),d?(c=["C",a.rightContX||a.plotX,a.rightContY||a.plotY,i||h,m||f,h,f],a.rightContX=a.rightContY=null):c=["M",h,f]):c=a.call(this,b,c,d),c}),w(b,"translate",function(a){var b=this.chart;if(a.call(this),b.polar&&(this.kdByAngle=b.tooltip&&b.tooltip.shared,!this.preventPostTranslate))for(a=this.points,b=a.length;b--;)this.toXY(a[b])}),w(b,"getGraphPath",function(a,b){var c=this;return this.chart.polar&&(b=b||this.points,this.options.connectEnds!==!1&&b[0]&&null!==b[0].y&&(this.connectEnds=!0,b.splice(b.length,0,b[0])),t(b,function(a){void 0===a.polarPlotY&&c.toXY(a)})),a.apply(this,[].slice.call(arguments,1))}),w(b,"animate",a),i.column&&(d=i.column.prototype,d.polarArc=function(a,b,c,d){var h=this.xAxis.center,f=this.yAxis.len;return this.chart.renderer.symbols.arc(h[0],h[1],f-b,null,{start:c,end:d,innerR:f-o(a,f)})},w(d,"animate",a),w(d,"translate",function(a){var d,h,f,b=this.xAxis,c=b.startAngleRad;if(this.preventPostTranslate=!0,a.call(this),b.isRadial)for(d=this.points,f=d.length;f--;)h=d[f],a=h.barX+c,h.shapeType="path",h.shapeArgs={d:this.polarArc(h.yBottom,h.plotY,a,a+h.pointWidth)},this.toXY(h),h.tooltipPos=[h.plotX,h.plotY],h.ttBelow=h.plotY>b.center[1]}),w(d,"alignDataLabel",function(a,c,d,i,h,f){this.chart.polar?(a=c.rectPlotX/Math.PI*180,null===i.align&&(i.align=a>20&&160>a?"left":a>200&&340>a?"right":"center"),null===i.verticalAlign&&(i.verticalAlign=45>a||a>315?"bottom":a>135&&225>a?"top":"middle"),b.alignDataLabel.call(this,c,d,i,h,f)):a.call(this,c,d,i,h,f)})),w(c,"getCoordinates",function(a,b){var c=this.chart,d={xAxis:[],yAxis:[]};return c.polar?t(c.axes,function(a){var f=a.isXAxis,g=a.center,i=b.chartX-g[0]-c.plotLeft,g=b.chartY-g[1]-c.plotTop;d[f?"xAxis":"yAxis"].push({axis:a,value:a.translate(f?Math.PI-Math.atan2(i,g):Math.sqrt(Math.pow(i,2)+Math.pow(g,2)),!0)})}):d=a.call(this,b),d})}()});