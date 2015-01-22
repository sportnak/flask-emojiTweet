/** @jsx React.DOM */
var height = 2, width = 3;

var Emoji = React.createClass({

	post: function(url){
		$.ajax({
			url: url,
			type:'POST',
			success: function(data){
				this.setState({data: data});
			}.bind(this),
			error: function(xhr, status, err) {
				console.error(url, status, err.toString());
			}.bind(this)
		});
	},

	render: function(){
		var postString = "/post/" + this.props.emoji.id

		return (
			<li style={{width:'100px', height:'100px;', display:'inline-block'}} onClick={function() {
					this.post(postString)
				}.bind(this)}>
				<a href={postString}><img src={this.props.emoji.location} style={{width:'100px', height:'100px;', display:'inline-block'}} ></img></a>
			</li>
		);
	}
})

var EmojiList = React.createClass({
	getInitialState: function(){
		return {
			currentPage: 1
		}
	},

	componentsWillReceiveProps: function(props){
		this.setState({
			currentPage:1
		})
	},

	render: function(){
		var page = this.getPage()
		var emojis1 = page.data1.map(function(emoji){
			return (
				<Emoji emoji={emoji}/>
			)
		})
		var emojis2 = page.data2.map(function(emoji){
			return (
				<Emoji emoji={emoji}/>
			)
		})
		var prev;
		if (page.currentPage > 1){
			prev = <a href="#" aria-label="Previous" onClick={page.handleClick(page.currentPage -1)}><span aria-hidden="true">«</span></a>
		} else {
			prev = <a href="#" aria-label="Previous"><span aria-hidden="true">«</span></a>
		}

		var nex;
		if (page.currentPage < page.numPages){
			next = <a href="#" aria-label="Previous" onClick={page.handleClick(page.currentPage + 1)}><span aria-hidden="true">»</span></a>
		} else {
			next = <a href="#" aria-label="Previous"><span aria-hidden="true">»</span></a>
		}

		return (
			<div>
				<nav> 
					<ul className="pagination pagination-lg">
						<li>
							{prev}
						</li>
						<li>
							{next}
						</li>
					</ul>
				</nav>
				<ul>
					{emojis1}
					<br></br>
					{emojis2}
				</ul>
			</div>
		)
		
	},

	getPage: function(){
		var start = height*width*(this.state.currentPage - 1);
		var end = start + (height*width);

		return {
			currentPage: this.state.currentPage,
			data1: this.props.data.slice(start,end/height),
			data2: this.props.data.slice(end/height, end),
			numPages: this.getNumPages(),
			handleClick: function(pageNum) {
				return function() {
					this.handlePageChange(pageNum)
				}.bind(this)
			}.bind(this)
		}
	},

	getNumPages: function(){
		return Math.ceil(this.props.data.length /(height*width))
	},

	handlePageChange: function(pageNum) {
		this.setState({currentPage: pageNum})
	}
})

var EmojiBox = React.createClass({
	getInitialState: function(){
		return {
			data:[]
		}
	},

	loadEmojisFromServer: function() {
		$.ajax({
			url: '/emojis',
			dataType: 'json',
			success: function(data){
				this.setState({data: data});
			}.bind(this),
			error: function(xhr, status, err) {
				console.error('/emojis', status, err.toString());
			}.bind(this)
		});
	},

	componentWillMount: function(){
		this.loadEmojisFromServer();
        setInterval(this.loadCommentsFromServer, this.props.pollInterval);
	},

	render: function(){
		return(
			<div>
				<EmojiList data={this.state.data}/>
			</div>
		)
	}
})

function pager(page) {
  var pageLinks = []
  if (page.currentPage > 1) {
  	pageLinks.push(<li><a href="#" aria-label="Previous"><span aria-hidden="true" onClick={page.handleClick(page.currentPage -1)}>«</span></a></li>)
    pageLinks.push(' ')
  }	
  if (page.currentPage < page.numPages) {
    pageLinks.push(' ')
    pageLinks.push(<span className="pageLink" onClick={page.handleClick(page.currentPage + 1)}>›</span>)
    if (page.currentPage < page.numPages - 1) {
      pageLinks.push(' ')
      pageLinks.push(<span className="pageLink" onClick={page.handleClick(page.numPages)}>»</span>)
    }
  }
  return <div className="pagination pagination-lg">{pageLinks}</div>
}

React.renderComponent(
	<EmojiBox/>,
	document.getElementById('crazy stuff')
);