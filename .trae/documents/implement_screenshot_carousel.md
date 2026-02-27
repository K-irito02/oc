# Plan: Implement 3D Carousel for Product Screenshots

## 1. Install Dependencies
- Install `swiper` library to handle the carousel functionality.
  - Command: `npm install swiper`

## 2. Create `ScreenshotGallery` Component
- Create a new file `src/components/ScreenshotGallery.tsx`.
- Import necessary Swiper modules: `Swiper`, `SwiperSlide`, `EffectCoverflow`, `Pagination`, `Navigation`, `Autoplay`.
- Import Swiper CSS styles.
- Implement the component with the following specifications:
  - **Layout**: Use `effect="coverflow"` for the 3D surround effect.
  - **Interaction**: Enable `grabCursor` for mouse dragging.
  - **Autoplay**: Configure `autoplay` with `delay` and `pauseOnMouseEnter: true` to stop rotation on hover.
  - **Navigation**: Enable `navigation` (prev/next buttons) and style them to be on the left/right sides.
  - **Styling**: Ensure the carousel fits within the parent container and images are styled correctly (rounded corners, etc.).
  - **Loop**: Enable `loop={true}` for continuous rotation.

## 3. Integrate into `ProductDetail` Page
- Edit `src/pages/ProductDetail/index.tsx`.
- Import the new `ScreenshotGallery` component.
- Replace the existing grid layout for screenshots with the `<ScreenshotGallery />` component.
- Pass `product.screenshots` as a prop.

## 4. Verification
- Verify that the carousel renders correctly.
- Test the auto-rotation and pause-on-hover behavior.
- Test the navigation buttons and mouse dragging.
