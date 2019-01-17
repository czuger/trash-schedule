require 'pp'
require 'date'
require 'odf-report'
require 'i18n'

require_relative 'lib/dates_handler'
require_relative 'lib/in_charge'

class BuildFile

  def initialize
    @dates = DatesHandler.new.read
    @in_charge = InCharge.new.read
  end

  def go
    report = ODFReport::Report.new('data/Courier model poubelles.odt') do |r|

      dw = @dates.dates_for_current_week

      pp dw

      r.add_field :date_jaune_out, dw.shift
      r.add_field :date_jaune_in, dw.shift
      r.add_field :date_bleue_out, dw.shift
      r.add_field :date_bleue_in, dw.shift

      r.add_field :resp_semaine_1, @in_charge.current_in_charge
      r.add_field :resp_semaine_2, @in_charge.next_in_charge
      r.add_field :resp_semaine_3, @in_charge.last_in_charge
    end

    report.generate('file.odt')
    @in_charge.save
  end

end

I18n.load_path = Dir['config/*.yml']
I18n.backend.load_translations
I18n.available_locales = [:fr]
I18n.locale = :fr

BuildFile.new.go