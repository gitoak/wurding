import { render } from '@testing-library/react';

import WebUi from './WebUi';

describe('WebUi', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<WebUi />);
    expect(baseElement).toBeTruthy();
  });
});
