require 'date'

cancel_dates = [ [3, 29], [ 4, 1, 2, 5, 8 ], [ 5, 1, 8, 13, 24, 27 ], [ 7, 14, 15 ],
                 [ 8, 15 ], [ 11, 1, 4, 11 ], [ 12, 25, 26 ] ]

add_dates = [
    [3, { j: [ 27 ], b: [ 31 ] }],
    [4, { j: [ 6 ], b: [ 9 ] }],
    [5, { j: [ 25 ], b: [ 14, 28 ] }],
    [7, { j: [], b: [ 16 ] }],
    [11, { j: [2], b: [ 5, 12 ] }]
]

year = 2021

exp_cancel_dates = []
cancel_dates.each do |group|
  month = group.shift
  group.each do |day|
    exp_cancel_dates << Date.new( year, month, day )
  end
end

exp_add_dates = {}
add_dates.each do |group|
  month = group.shift
  d = group.shift
  d.each do |typ, days|
    days.each do |day|
      exp_add_dates[Date.new( year, month, day )] = (typ == :j ? 'jaune' : 'bleue')
    end
  end
end

final_dates = exp_add_dates

monday = Date.new( 2021, 3, 1 )
1.upto( 44 ).each do
  tuesday = monday + 3

  # puts monday

  final_dates[monday] = 'jaune' unless exp_cancel_dates.include?(monday)
  final_dates[tuesday] = 'bleue' unless exp_cancel_dates.include?(tuesday)

  monday = monday + 7
end

final_dates.keys.sort.each do |k|
  puts "#{k}\t Poubelle #{final_dates[k]}"
end