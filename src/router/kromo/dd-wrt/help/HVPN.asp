<% do_hpagehead("vpn.titl"); %>
	<body class="help-bg">
		<div id="header">
			<div class="logo"> </div>
			<div class="navig"><a href="index.asp">Index</a> | <a href="javascript:self.close();"><% tran("sbutton.clos"); %></a></div>
		</div>
		<div id="content">
			<h2><% tran("vpn.legend"); %></h2>
			<dl>
				<% tran("hvpn.page1"); %>
				<dt><% tran("vpn.ipsec"); %></dt>
				<% tran("hvpn.page2"); %>
				<dt><% tran("vpn.pptp"); %></dt>
				<% tran("hvpn.page3"); %>
				<dt><% tran("vpn.l2tp"); %></dt>
				<% tran("hvpn.page4"); %>
			</dl>
		</div>
		<div class="also">
			<h4><% tran("share.seealso"); %></h4>
			<ul>
				<li><a href="HForwardSpec.asp"><% tran("bmenu.applicationspforwarding"); %></a></li>
				<li><a href="HManagement.asp"><% tran("bmenu.adminManagement"); %></a></li>
			</ul>
		</div>
	</body>
</html>
