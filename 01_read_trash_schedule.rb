# utiliser https://convertio.co/fr/pdf-html/ pour la conversion pdf -> html

require 'yaml'
require 'pp'


def read_file( name )
  data = YAML.load_file("data2/#{name}.yaml")
  a = []

  data.each do |k, v|
    year, month = k.split( '-' )
    a << v.map{ |day| Date.parse( "#{year}-#{month}-#{day}" ) }
  end

  a.flatten
end

bleu = read_file( :bleu )
jaune = read_file( :jaune )

mix = []

while bleu.length > 0
  b = bleu.shift
  j = jaune.shift

  mix << { jaune: j, bleue: b }
end

File.open( 'data2/mixed.yaml', 'w' ) do |f|
  f.write mix.to_yaml
end
