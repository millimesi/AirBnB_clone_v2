# Define the class for web server setup
class web_server {
  package { 'nginx':
    ensure => installed,
  }

  service { 'nginx':
    ensure  => running,
    enable  => true,
    require => Package['nginx'],
  }

  file { '/data/web_static/releases/test':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }

  file { '/data/web_static/shared':
    ensure => directory,
    owner  => 'ubuntu',
    group  => 'ubuntu',
    mode   => '0755',
  }

  file { '/data/web_static/releases/test/index.html':
    ensure  => present,
    owner   => 'ubuntu',
    group   => 'ubuntu',
    mode    => '0644',
    content => '<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>',
  }

  file { '/data/web_static/current':
    ensure => link,
    target => '/data/web_static/releases/test/',
    owner  => 'ubuntu',
    group  => 'ubuntu',
  }

  file { '/etc/nginx/sites-available/default':
    ensure  => present,
    content => template('web_server/nginx_config.erb'),
    notify  => Service['nginx'],
  }
}
