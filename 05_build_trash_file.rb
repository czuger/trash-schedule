require 'pp'
require 'date'
require 'odf-report'
require 'i18n'
require 'yaml'
require 'ostruct'

require_relative 'lib/dates_handler'
require_relative 'lib/in_charge'

class BuildFile

  def initialize
    # @dates = DatesHandler.new.read
    # @in_charge = InCharge.new.read

    @in_charge = [ 'Etage 1', 'Etage 0', 'Etage 3', 'Etage 2' ]
  end

  def go
    report = ODFReport::Report.new('data2/Courier model poubelles.odt') do |r|

      mixed_dates = YAML.load_file( 'data2/mixed.yaml' )

      mixed_dates.select!{ |e| e[:blue].to_time.to_i > Time.now.to_i }

      mixed_dates = mixed_dates.shift( 26 )

      mixed_dates.map!{ |e| OpenStruct.new( date: e[:blue],
                                            blue: I18n.l(e[:blue], format: '%A, %-d %B').humanize,
                                            yellow:  I18n.l(e[:yellow], format: '%A, %-d %B').humanize,
                                            responsable: get_floor ) }

      r.add_table('Tableau1', mixed_dates, :header=>true) do |t|
        t.add_column(:responsable)
        t.add_column(:yellow)
        t.add_column(:blue)
      end
    end

    report.generate('data2/Trash schedule.odt')
    # @in_charge.save
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