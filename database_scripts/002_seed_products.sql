-- Seed category hierarchy
INSERT INTO categories (name, slug, level, sort_order)
VALUES
  ('Wood Works', 'wood-works', 1, 1),
  ('Household Use', 'household-use', 1, 2),
  ('Construction Works', 'construction-works', 1, 3),
  ('Automotive', 'automotive', 1, 4),
  ('Hand Tools', 'hand-tools', 1, 5),
  ('Electrical', 'electrical', 1, 6)
ON CONFLICT (slug) DO UPDATE
SET
  name = EXCLUDED.name,
  level = EXCLUDED.level,
  sort_order = EXCLUDED.sort_order;

INSERT INTO categories (name, slug, parent_id, level, sort_order)
SELECT child.name, child.slug, parent.id, 2, child.sort_order
FROM (
  VALUES
    ('wood-works', 'Power Cutting Tools', 'power-cutting-tools', 1),
    ('wood-works', 'Surface Finishing', 'surface-finishing', 2),
    ('household-use', 'Home Power Solutions', 'home-power-solutions', 1),
    ('household-use', 'Tool Kits', 'tool-kits', 2),
    ('construction-works', 'Cutting & Grinding', 'cutting-and-grinding', 1),
    ('construction-works', 'Drilling & Demolition', 'drilling-and-demolition', 2),
    ('automotive', 'Garage Power Tools', 'garage-power-tools', 1),
    ('automotive', 'Air & Charging', 'air-and-charging', 2),
    ('hand-tools', 'Fastening Tools', 'fastening-tools', 1),
    ('hand-tools', 'Measuring & Grip', 'measuring-and-grip', 2),
    ('electrical', 'Testing Equipment', 'testing-equipment', 1),
    ('electrical', 'Repair Tools', 'repair-tools', 2)
) AS child(parent_slug, name, slug, sort_order)
JOIN categories parent ON parent.slug = child.parent_slug
ON CONFLICT (slug) DO UPDATE
SET
  name = EXCLUDED.name,
  parent_id = EXCLUDED.parent_id,
  level = EXCLUDED.level,
  sort_order = EXCLUDED.sort_order;

INSERT INTO categories (name, slug, parent_id, level, sort_order)
SELECT leaf.name, leaf.slug, parent.id, 3, leaf.sort_order
FROM (
  VALUES
    ('power-cutting-tools', 'Circular Saw', 'circular-saw', 1),
    ('power-cutting-tools', 'Jig Saw', 'jig-saw', 2),
    ('surface-finishing', 'Planer', 'planer', 1),
    ('surface-finishing', 'Sander', 'sander', 2),
    ('home-power-solutions', 'Generator', 'generator', 1),
    ('home-power-solutions', 'Cordless Drill', 'cordless-drill', 2),
    ('tool-kits', 'Hand Tools Set', 'hand-tools-set', 1),
    ('tool-kits', 'Compact Toolbox', 'compact-toolbox', 2),
    ('cutting-and-grinding', 'Angle Grinders', 'angle-grinders', 1),
    ('cutting-and-grinding', 'Cut Off Saw', 'cut-off-saw', 2),
    ('drilling-and-demolition', 'Rotary Hammer', 'rotary-hammer', 1),
    ('drilling-and-demolition', 'Demolition Hammer', 'demolition-hammer', 2),
    ('garage-power-tools', 'Impact Wrench', 'impact-wrench', 1),
    ('garage-power-tools', 'Polisher', 'polisher', 2),
    ('air-and-charging', 'Air Compressor', 'air-compressor', 1),
    ('air-and-charging', 'Battery Charger', 'battery-charger', 2),
    ('fastening-tools', 'Screwdrivers', 'screwdrivers', 1),
    ('fastening-tools', 'Wrenches', 'wrenches', 2),
    ('measuring-and-grip', 'Pliers', 'pliers', 1),
    ('measuring-and-grip', 'Tape Measures', 'tape-measures', 2),
    ('testing-equipment', 'Multimeters', 'multimeters', 1),
    ('testing-equipment', 'Electrical Testers', 'electrical-testers', 2),
    ('repair-tools', 'Heat Gun', 'heat-gun', 1),
    ('repair-tools', 'Soldering Iron', 'soldering-iron', 2)
) AS leaf(parent_slug, name, slug, sort_order)
JOIN categories parent ON parent.slug = leaf.parent_slug
ON CONFLICT (slug) DO UPDATE
SET
  name = EXCLUDED.name,
  parent_id = EXCLUDED.parent_id,
  level = EXCLUDED.level,
  sort_order = EXCLUDED.sort_order;

-- Seed products data and connect each product to a leaf category
WITH seed_products AS (
  SELECT *
  FROM (
    VALUES
      ('Crown CT15028 Angle Grinder', 'crown-ct15028-angle-grinder', 'Professional 4.5" angle grinder with 850W motor. Perfect for cutting, grinding, and polishing metal surfaces.', 'Crown', 'Construction Works', 'angle-grinders', 4500::DECIMAL(10,2), 5200::DECIMAL(10,2), '/images/product-grinder.jpg', 4.5::DECIMAL(2,1), 24, 'Best Seller', true),
      ('Crown CT13503 Heat Gun', 'crown-ct13503-heat-gun', 'Industrial heat gun with variable temperature control. Ideal for paint stripping, shrink wrapping, and thawing.', 'Crown', 'Electrical', 'heat-gun', 2800::DECIMAL(10,2), 3200::DECIMAL(10,2), '/images/product-heatgun.jpg', 4.4::DECIMAL(2,1), 21, NULL, true),
      ('Crown CT20001 Rotary Hammer', 'crown-ct20001-rotary-hammer', '26mm rotary hammer drill with SDS-plus chuck. Features 3 modes: drilling, hammer drilling, and chiseling.', 'Crown', 'Construction Works', 'rotary-hammer', 7500::DECIMAL(10,2), 8200::DECIMAL(10,2), '/images/product-hammer.jpg', 4.6::DECIMAL(2,1), 32, 'Popular', true),
      ('TOTAL TD2051126 Impact Drill', 'total-td2051126-impact-drill', '13mm impact drill with 750W motor. Includes variable speed control and reverse function.', 'TOTAL', 'Household Use', 'cordless-drill', 3200::DECIMAL(10,2), 3800::DECIMAL(10,2), '/images/product-drill.jpg', 4.3::DECIMAL(2,1), 18, 'Sale', true),
      ('TOTAL TS2061256 Orbital Sander', 'total-ts2061256-orbital-sander', 'Random orbital sander with dust collection. Perfect for fine finishing on wood and metal surfaces.', 'TOTAL', 'Wood Works', 'sander', 2500::DECIMAL(10,2), 2900::DECIMAL(10,2), '/images/product-sander.jpg', 4.1::DECIMAL(2,1), 12, NULL, true),
      ('TOTAL TS206856 Jigsaw', 'total-ts206856-jigsaw', 'Variable speed jigsaw with pendulum action. Cuts wood, metal, and plastic with precision.', 'TOTAL', 'Wood Works', 'jig-saw', 3500::DECIMAL(10,2), 4000::DECIMAL(10,2), '/images/product-jigsaw.jpg', 4.2::DECIMAL(2,1), 15, 'New', true),
      ('BOSCH GSB 500 RE Drill', 'bosch-gsb-500-re-drill', 'Professional impact drill with 500W motor. Features forward/reverse, variable speed, and auxiliary handle.', 'BOSCH', 'Household Use', 'cordless-drill', 6800::DECIMAL(10,2), 7500::DECIMAL(10,2), '/images/product-saw.jpg', 4.8::DECIMAL(2,1), 42, 'Premium', true),
      ('BOSCH GWS 600 Angle Grinder', 'bosch-gws-600-angle-grinder', '4" angle grinder with 670W motor. Lightweight design for extended use. Includes safety guard.', 'BOSCH', 'Construction Works', 'angle-grinders', 5500::DECIMAL(10,2), 6200::DECIMAL(10,2), '/images/product-grinder.jpg', 4.7::DECIMAL(2,1), 38, 'Top Rated', true),
      ('BOSCH GST 650 Jigsaw', 'bosch-gst-650-jigsaw', 'Professional jigsaw with 450W motor. Features SDS blade system and blowing function.', 'BOSCH', 'Wood Works', 'jig-saw', 5800::DECIMAL(10,2), 6500::DECIMAL(10,2), '/images/product-jigsaw.jpg', 4.5::DECIMAL(2,1), 28, NULL, true),
      ('INGCO Circular Saw CS18528', 'ingco-circular-saw-cs18528', '7" circular saw with 1400W motor. Features adjustable cutting depth and bevel capacity up to 45 degrees.', 'INGCO', 'Wood Works', 'circular-saw', 5500::DECIMAL(10,2), NULL, '/images/product-wrench.jpg', 4.2::DECIMAL(2,1), 15, 'New', true),
      ('INGCO Impact Wrench IW10508', 'ingco-impact-wrench-iw10508', '1/2" electric impact wrench with 1050W motor. Max torque 550N.m. Perfect for automotive work.', 'INGCO', 'Automotive', 'impact-wrench', 6200::DECIMAL(10,2), 6800::DECIMAL(10,2), '/images/product-wrench.jpg', 4.3::DECIMAL(2,1), 22, NULL, true),
      ('INGCO Cordless Drill CDLI20028', 'ingco-cordless-drill-cdli20028', '20V cordless drill with 2 Li-ion batteries. Features 2-speed gearbox and LED work light.', 'INGCO', 'Household Use', 'cordless-drill', 7800::DECIMAL(10,2), 8500::DECIMAL(10,2), '/images/product-drill.jpg', 4.4::DECIMAL(2,1), 35, 'Best Value', true),
      ('DEWALT DWD024 Drill', 'dewalt-dwd024-drill', 'Professional 13mm percussion drill with 750W motor. Features metal gear housing and rubber grip.', 'DEWALT', 'Construction Works', 'rotary-hammer', 8500::DECIMAL(10,2), 9200::DECIMAL(10,2), '/images/product-drill.jpg', 4.9::DECIMAL(2,1), 56, 'Premium', true),
      ('DEWALT DWE4115 Angle Grinder', 'dewalt-dwe4115-angle-grinder', '4.5" angle grinder with 950W motor. Features no-volt release switch and spindle lock.', 'DEWALT', 'Construction Works', 'angle-grinders', 9200::DECIMAL(10,2), 10500::DECIMAL(10,2), '/images/product-grinder.jpg', 4.8::DECIMAL(2,1), 48, 'Professional', true),
      ('DEWALT DCS391 Circular Saw', 'dewalt-dcs391-circular-saw', '20V MAX cordless circular saw. 6.5" blade with 5150 RPM. Lightweight at only 3.1kg.', 'DEWALT', 'Wood Works', 'circular-saw', 15500::DECIMAL(10,2), 17000::DECIMAL(10,2), '/images/product-saw.jpg', 4.7::DECIMAL(2,1), 41, 'Top Choice', true),
      ('MAKITA HR2470 Rotary Hammer', 'makita-hr2470-rotary-hammer', '24mm rotary hammer with 780W motor. Features 3-mode operation and torque limiter clutch.', 'MAKITA', 'Construction Works', 'rotary-hammer', 12500::DECIMAL(10,2), 14000::DECIMAL(10,2), '/images/product-hammer.jpg', 4.7::DECIMAL(2,1), 38, 'Top Rated', true),
      ('MAKITA 9556NB Angle Grinder', 'makita-9556nb-angle-grinder', '4" angle grinder with 840W motor. Features labyrinth construction and super joint system.', 'MAKITA', 'Construction Works', 'angle-grinders', 7800::DECIMAL(10,2), 8500::DECIMAL(10,2), '/images/product-grinder.jpg', 4.6::DECIMAL(2,1), 45, 'Professional', true),
      ('MAKITA BO5030 Orbital Sander', 'makita-bo5030-orbital-sander', '5" random orbit sander with 300W motor. Features variable speed and dust collection.', 'MAKITA', 'Wood Works', 'sander', 6500::DECIMAL(10,2), 7200::DECIMAL(10,2), '/images/product-sander.jpg', 4.5::DECIMAL(2,1), 29, NULL, true),
      ('Professional Wrench Set 12pc', 'professional-wrench-set-12pc', 'Chrome vanadium steel combination wrench set. Sizes 8-24mm. Includes carrying case.', 'TOTAL', 'Hand Tools', 'wrenches', 2200::DECIMAL(10,2), 2500::DECIMAL(10,2), '/images/product-wrench.jpg', 4.3::DECIMAL(2,1), 33, NULL, true),
      ('Screwdriver Set 8pc', 'screwdriver-set-8pc', 'Precision screwdriver set with magnetic tips. Includes Phillips and flathead in various sizes.', 'INGCO', 'Hand Tools', 'screwdrivers', 850::DECIMAL(10,2), 1000::DECIMAL(10,2), '/images/product-wrench.jpg', 4.1::DECIMAL(2,1), 28, NULL, true),
      ('Digital Multimeter DT830B', 'digital-multimeter-dt830b', 'Digital multimeter for measuring voltage, current, and resistance. LCD display with backlight.', 'TOTAL', 'Electrical', 'multimeters', 650::DECIMAL(10,2), 800::DECIMAL(10,2), '/images/product-heatgun.jpg', 4.0::DECIMAL(2,1), 45, NULL, true),
      ('Soldering Iron 60W', 'soldering-iron-60w', 'Temperature adjustable soldering iron. Includes stand and solder wire. Fast heating.', 'INGCO', 'Electrical', 'soldering-iron', 450::DECIMAL(10,2), 550::DECIMAL(10,2), '/images/product-heatgun.jpg', 4.2::DECIMAL(2,1), 38, NULL, true),
      ('Car Battery Charger 12V', 'car-battery-charger-12v', 'Automatic car battery charger with LED indicators. Suitable for all 12V lead-acid batteries.', 'TOTAL', 'Automotive', 'battery-charger', 1800::DECIMAL(10,2), 2200::DECIMAL(10,2), '/images/product-drill.jpg', 4.3::DECIMAL(2,1), 19, NULL, true),
      ('Air Compressor 25L', 'air-compressor-25l', '25 liter air compressor with 2HP motor. Max pressure 8 bar. Includes air hose and accessories.', 'Crown', 'Automotive', 'air-compressor', 12000::DECIMAL(10,2), 13500::DECIMAL(10,2), '/images/product-grinder.jpg', 4.5::DECIMAL(2,1), 27, 'Popular', true)
  ) AS product(name, slug, description, brand, category, category_slug, price, original_price, image, rating, reviews_count, badge, in_stock)
)
INSERT INTO products (
  name,
  slug,
  description,
  brand,
  category,
  category_id,
  price,
  original_price,
  image,
  rating,
  reviews_count,
  badge,
  in_stock
)
SELECT
  product.name,
  product.slug,
  product.description,
  product.brand,
  product.category,
  categories.id,
  product.price,
  product.original_price,
  product.image,
  product.rating,
  product.reviews_count,
  product.badge,
  product.in_stock
FROM seed_products product
LEFT JOIN categories ON categories.slug = product.category_slug
ON CONFLICT (slug) DO UPDATE
SET
  name = EXCLUDED.name,
  description = EXCLUDED.description,
  brand = EXCLUDED.brand,
  category = EXCLUDED.category,
  category_id = EXCLUDED.category_id,
  price = EXCLUDED.price,
  original_price = EXCLUDED.original_price,
  image = EXCLUDED.image,
  rating = EXCLUDED.rating,
  reviews_count = EXCLUDED.reviews_count,
  badge = EXCLUDED.badge,
  in_stock = EXCLUDED.in_stock;
