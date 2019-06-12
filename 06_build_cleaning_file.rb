require 'pp'
require 'date'
require 'odf-report'
require 'i18n'
require 'yaml'
require 'ostruct'

class BuildFile

  def initialize
    @in_charge = [ 'Etage 1', 'Etage 3', 'Etage 2' ]
  end

  def go
    report = ODFReport::Report.new('data2/Cleaning schedule model.odt') do |r|

      next_sunday = ( Date.today + ( 7 - Date.today.wday ) )

      dates = 0.upto( 24 ).map{ |i| next_sunday + ( i*7 ) }

      dates.map!{ |e| OpenStruct.new( cleaning: I18n.l( e, format: '%A, %-d %B'),
                                            responsable: get_floor ) }

      r.add_table('Tableau1', dates, :header=>true) do |t|
        t.add_column(:responsable)
        t.add_column(:cleaning)
      end
    end

    report.generate('data2/Cleaning schedule.odt')
  end

  def get_floor
    f = @in_charge.shift
    @in_charge << f
    f
  end

end

I18n.load_path = Dir['config/*.yml']
I18n.backend.load_translations
I18n.available_locales = [:fr]
I18n.locale = :fr

BuildFile.new.go