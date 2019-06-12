# utiliser https://convertio.co/fr/pdf-html/ pour la conversion pdf -> html

require 'yaml'
require 'pp'


def read_file( name )
  data = YAML.load_file("data2/#{name}.yaml")
  a = []

  data.each do |k, v|
    year, month = k.split( '-' )
    p year, month
    a << v.map{ |day| Date.parse( "#{year}-#{month}-#{day}" ) }
  end

  a.flatten
end

blue = read_file( :blue )
yellow = read_file( :yellow )

mix = []

while blue.length > 0
  b = blue.shift
  j = yellow.shift

  mix << { yellow: j, blue: b }
end

File.open( 'data2/mixed.yaml', 'w' ) do |f|
  f.write mix.to_yaml
end
